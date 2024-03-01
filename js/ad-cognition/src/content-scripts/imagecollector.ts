import { MESSAGE_TYPES, Prediction } from 'Common/constants/common';

export class ImageCollector {
    protected TEXT_DIV_CLASSNAME: string;

    protected MIN_IMG_SIZE: number;

    protected IMAGE_SIZE: number;

    protected images: HTMLImageElement[] = [];

    protected MIN_CONFIDENCE: number;

    public DEBUG_MODE: boolean;

    public CNN_ENABLED: boolean;

    public CLIP_ENABLED: boolean;

    constructor(debug_mode: boolean, cnn_enabled: boolean, clip_enabled: boolean, imgArray: HTMLImageElement[]) {
        this.IMAGE_SIZE = 100;
        this.MIN_IMG_SIZE = 100;
        this.TEXT_DIV_CLASSNAME = '';

        this.DEBUG_MODE = debug_mode;
        this.CNN_ENABLED = cnn_enabled;
        this.CLIP_ENABLED = clip_enabled;
        this.MIN_CONFIDENCE = 0.2;
        this.images = imgArray;
    }

    getAdTextContent(prediction: Prediction) {
        if (typeof prediction === 'number') {
            return `CNN: ${Math.floor(Math.abs(prediction - 1) * 100)}% AD\n`;
        } else {
            return `CLIP: ${(prediction[0] * 100).toFixed(1)}% AD, ${(prediction[1] * 100).toFixed(1)}% NON AD\n`;
        }
    }

    public send() {
        // Function to handle each image
        const handleImage = (image: HTMLImageElement) => {
            const source = image.getAttribute('src') || image.getAttribute('data-src');
            if (source && image.complete) {
                this.analyzeImage(source);
            } else {
                image.addEventListener('load', () => {
                    if (source) this.analyzeImage(source);
                });
            }
        };

        // Create a new IntersectionObserver
        const observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                // If the element is in the viewport
                if (entry.isIntersecting) {
                    handleImage(entry.target as HTMLImageElement);
                    observer.unobserve(entry.target);
                }
            });
        });

        // Observe all images on the page
        const images = Array.from(document.getElementsByTagName('img'));
        images.forEach(image => observer.observe(image));

        // Handle images inside iframes
        const iframes = document.getElementsByTagName('iframe');
        for (let i = 0; i < iframes.length; i++) {
            try {
                const iframeImages = iframes[i]?.contentDocument?.getElementsByTagName('img');
                Array.from(iframeImages!).forEach(image => observer.observe(image));
            } catch (error) {
                console.log('Could not access iframe content:', error);
            }
        }
    }

    isAd(prediction: Prediction) {
        if (!prediction) return;

        if (typeof prediction === 'number') {
            return prediction < 0.5;
        } else {
            return (prediction[0] > this.MIN_CONFIDENCE) && (prediction[0] > prediction[1]);
        }
    }

    public removeImage(prediction: Prediction, url: string) {
        const imgNode = this.getImageBySrc(url);
        if (imgNode && this.isAd(prediction)) {
            const parentElement = imgNode.parentElement;

            if (parentElement && parentElement.children.length === 1) {
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

    markImage(prediction: Prediction, url: string) {

        if (!prediction) {
            return;
        }

        const overlayCreated = document.querySelector('.debugOverlay' + url.replace(/[^a-zA-Z0-9_-]/g, ''));
        const containerCreated = document.querySelector('.debugContainer' + url.replace(/[^a-zA-Z0-9_-]/g, ''));
        const adTextCreated: HTMLDivElement | null = document.querySelector('.adText' + url.replace(/[^a-zA-Z0-9_-]/g, ''));

        // Create a div element to wrap the img and overlay
        const container = document.createElement('div');
        if (!containerCreated) {
            container.className = 'debugContainer' + url.replace(/[^a-zA-Z0-9_-]/g, '');
            Object.assign(container.style, {
                position: 'relative',
                display: 'inline-block',
            });
        }

        // Create an overlay div for the white square background
        const overlay = document.createElement('div');
        if (!overlayCreated) {
            overlay.className = 'debugOverlay' + url.replace(/[^a-zA-Z0-9_-]/g, '');
            Object.assign(overlay.style, {
                position: 'absolute',
                top: '0',
                left: '0',
                width: '100%',
                height: '100%',
                backgroundColor: 'white',
                opacity: '0.7',
            });
        }

        const adText = document.createElement('div');
        if (!adTextCreated) {
            adText.className = 'adText' + url.replace(/[^a-zA-Z0-9_-]/g, '');
            Object.assign(adText.style, {
                position: 'absolute',
                fontSize: '16px',
                color: 'black',
            });
            adText.innerText = this.getAdTextContent(prediction);
        } else {
            adTextCreated.innerText += this.getAdTextContent(prediction);
        }


        // Create a clone of the img element
        const imgClone: any = this.getImageBySrc(url)?.cloneNode(
            true,
        );

        // Append the elements to the container
        if (imgClone) {
            if (!containerCreated) container.appendChild(imgClone);
            if (!overlayCreated) container.appendChild(overlay);
        }

        if (overlayCreated) {
            overlayCreated.appendChild(adText);
        } else {
            overlay.appendChild(adText);
        }

        // Replace the original img element with the container
        const img: any = this.getImageBySrc(url);
        !containerCreated && img.parentNode.replaceChild(container, img);
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

                if (imageData !== undefined && this.CNN_ENABLED) {
                    const predictionInfo = await chrome.runtime.sendMessage({
                        type: MESSAGE_TYPES.SEND_IMAGES_CNN,
                        data: {
                            rawImageData: Array.from(imageData.data),
                            width: img.width,
                            height: img.height,
                            url: img.src,
                        },
                    });
                    if (this.DEBUG_MODE) {
                        this.markImage(predictionInfo.prediction, predictionInfo.url);
                    } else {
                        this.removeImage(predictionInfo.prediction, img.src);
                    }
                }

                if (this.CLIP_ENABLED) {
                    const clip_prediction = await chrome.runtime.sendMessage({
                        type: MESSAGE_TYPES.SEND_IMAGES_CLIP,
                        data: {
                            src: img.src,
                        },
                    });
                    if (this.DEBUG_MODE) {
                        this.markImage(clip_prediction, img.src);
                    } else {
                        this.removeImage(clip_prediction, img.src);
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
