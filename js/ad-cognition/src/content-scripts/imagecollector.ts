import { MESSAGE_TYPES } from 'Common/constants/common';
import { log } from 'Common/logger';

export class ImageCollector {
    protected TEXT_DIV_CLASSNAME: string;

    protected MIN_IMG_SIZE: number;

    protected IMAGE_SIZE: number;

    protected images: HTMLImageElement[] = [];

    public DEBUG_MODE: boolean;

    constructor(debug_mode: boolean) {
        this.IMAGE_SIZE = 100;
        this.MIN_IMG_SIZE = 100;
        this.TEXT_DIV_CLASSNAME = '';
        this.DEBUG_MODE = debug_mode;
    }

    public send() {
        this.images = ImageCollector.getImagesElements();

        const loadNextImage = (index: number) => {
            if (index >= this.images.length) {
                // All images have been loaded
                return;
            }

            const image = this.images[index];
            if (image !== null) {
                if (image.complete) {
                    this.analyzeImage(image.src);
                    loadNextImage(index + 1); // Load the next image
                } else {
                    image.addEventListener('load', () => {
                        this.analyzeImage(image.src);
                        loadNextImage(index + 1); // Load the next image
                    });
                }
            } else {
                loadNextImage(index + 1); // Load the next image
            }
        };

        loadNextImage(0); // Start loading the first image
    }

    public removeImage(prediction: number, url: string) {
        const imgNode = this.getImageBySrc(url);
        if (imgNode && prediction === 0) {
            let { parentElement } = imgNode;

            // Keep deleting parent elements as long as the child is the only element
            while (parentElement && parentElement.children.length === 1) {
                parentElement = parentElement.parentElement;
            }

            if (parentElement) {
                parentElement.remove(); // Remove the parent element
            }
        }
    }

    static getImagesElements() {
        return Array.from(document.querySelectorAll('img'));
    }

    // eslint-disable-next-line class-methods-use-this
    getImageBySrc(src: string) {
        return Array.from(document.querySelectorAll('img')).find(
            (img) => img.src === src,
        );
    }

    markImage(prediction: any) {
        if (!prediction) {
            return;
        }
        // Create a div element to wrap the img and overlay
        const container = document.createElement('div');
        container.style.position = 'relative';
        container.style.display = 'inline-block';

        // Create a clone of the img element
        const imgClone: any = this.getImageBySrc(prediction.url)?.cloneNode(
            true,
        );

        // Create an overlay div for the white square background
        const overlay = document.createElement('div');
        overlay.style.position = 'absolute';
        overlay.style.top = '0';
        overlay.style.left = '0';
        overlay.style.width = '100%';
        overlay.style.height = '100%';
        overlay.style.backgroundColor = prediction.prediction < 0.5 ? 'red' : 'white'; // White with 0.5 opacity
        overlay.style.opacity = '0.7'; // White with 0.5 opacity

        // Create the 'AD' text element
        const adText = document.createElement('div');
        adText.style.position = 'absolute';
        adText.style.top = '50%'; // Adjust as needed to center vertically
        adText.style.left = '50%'; // Adjust as needed to center horizontally
        adText.style.transform = 'translate(-50%, -50%)';
        adText.style.fontSize = '24px'; // Adjust the font size as needed
        adText.style.color = prediction.prediction < 0.5 ? 'white' : 'black'; // Text color
        adText.style.fontWeight = 'bold'; // Font weight
        adText.textContent = `${Math.floor(
            Math.abs(prediction.prediction - 1) * 100,
        )}% AD`;
        // adText.textContent = prediction.prediction < 0.5 ? 'AD' : 'NOT AD';

        // Append the elements to the container
        if (imgClone) {
            container.appendChild(imgClone);
            container.appendChild(overlay);
            overlay.appendChild(adText);
        }

        // Replace the original img element with the container
        const img: any = this.getImageBySrc(prediction.url);
        img.parentNode.replaceChild(container, img);
    }

    analyzeImage(src: string) {
        // Load image (with crossOrigin set to anonymouse so that it can be used in a
        // canvas later).
        const img = new Image();
        img.crossOrigin = 'anonymous';
        // img.onerror = function (e) {
        // };
        img.onload = async () => {
            if (
                (img.height && img.height > this.MIN_IMG_SIZE)
                || (img.width && img.width > this.MIN_IMG_SIZE)
            ) {
                img.width = this.IMAGE_SIZE;
                img.height = this.IMAGE_SIZE;
                // When image is loaded, render it to a canvas and send its ImageData back
                // to the service worker.
                const canvas = new OffscreenCanvas(img.width, img.height);
                const ctx = canvas.getContext('2d');
                ctx?.drawImage(img, 0, 0);
                const imageData = ctx?.getImageData(
                    0,
                    0,
                    img.width,
                    img.height,
                );
                if (imageData !== undefined) {
                    const prediction = await chrome.runtime.sendMessage({
                        type: MESSAGE_TYPES.SEND_IMAGES,
                        data: {
                            rawImageData: Array.from(imageData.data),
                            width: img.width,
                            height: img.height,
                            url: img.src,
                        },
                    });
                    if (this.DEBUG_MODE) {
                        this.markImage(prediction);
                    } else {
                        this.removeImage(prediction, img.src);
                    }
                }
            }
            // Fail out if either dimension is less than MIN_IMG_SIZE.
        };
        img.src = src;
    }

    init() {
        window.onload = () => this.send();
        chrome.runtime.onMessage.addListener((message) => {
            if (!message) {
                return;
            }

            switch (message.type) {
                case MESSAGE_TYPES.PREDICTION:
                    this.removeImage(message.prediction, message.url);
                    break;

                case MESSAGE_TYPES.ANALYZE_IMAGE:
                    this.analyzeImage(message.data.url);
                    break;
                default:
                    break;
            }
        });
    }
}
