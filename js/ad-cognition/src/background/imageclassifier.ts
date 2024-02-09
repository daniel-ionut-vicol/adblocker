import * as tf from '@tensorflow/tfjs';

import { log } from 'Common/logger';
import { MESSAGE_TYPES } from 'Common/constants/common';

export class ImageClassifier {
    // Size of the image expected by the model.
    static IMAGE_SIZE = 256;

    // How many predictions to take.
    static TOPK_PREDICTIONS = 2;

    static FIVE_SECONDS_IN_MS = 5000;

    pathToModel = '';

    static model: any;

    constructor(pathToModel: string) {
        this.pathToModel = pathToModel;
        this.loadModel();
    }

    async loadModel() {
        // const startTime = performance.now();

        try {
            ImageClassifier.model = await tf.loadLayersModel(this.pathToModel);
            // Warms up the model by causing intermediate tensor values
            // to be built and pushed to GPU.
            tf.tidy(() => {
                ImageClassifier.model.predict(
                    tf.zeros([1, ImageClassifier.IMAGE_SIZE, ImageClassifier.IMAGE_SIZE, 3]),
                );
            });
            // const totalTime = Math.floor(performance.now() - startTime);
        } catch (e) {
            log.error('Unable to load model', e);
        }
    }

    static preprocessImage(imageData: ImageData) {
        const IMAGE_MAX_PIXEL_VALUE = 255; // Max pixel value for 8-bit channels

        return tf.tidy(() => {
            // Convert the imageData object to a tensor
            const imageTensor = tf.browser.fromPixels(imageData);

            // Check if the image is in grayscale
            const isGrayscale = imageTensor.shape[2] === 1;

            // Convert to RGB color space if the image is grayscale or has 1 channel
            const rgbImage = isGrayscale
                ? tf.image.grayscaleToRGB(imageTensor)
                : imageTensor;

            // Resize the image tensor to the desired size
            const resizedImage = tf.image.resizeBilinear(rgbImage, [
                this.IMAGE_SIZE,
                this.IMAGE_SIZE,
            ]);

            // Normalize the image by scaling pixel values to the range [0, 1]
            const normalized = resizedImage.div(IMAGE_MAX_PIXEL_VALUE);

            // Add a batch dimension
            return normalized.expandDims(0);
        });
    }

    public static async processInput(rawImageData: any, width: number, height: number, url: string) {
        if (!rawImageData) {
            log.error(
                'Failed to get image  The image might be too small or failed to load.',
            );
            return;
        }

        const imageData = new ImageData(
            Uint8ClampedArray.from(rawImageData),
            width,
            height,
        );

        let messageToSend: Object = {};

        const result = await ImageClassifier.analyzeImage(
            imageData,
            url,
        );

        messageToSend = {
            type: MESSAGE_TYPES.PREDICTION,
            url,
            prediction: result?.prediction,
        };

        return messageToSend;
    }

    public static async analyzeImage(
        imageData: ImageData,
        url: string,
    ): Promise<Prediction> {
        // const startTime = performance.now();

        const preprocessedImage = this.preprocessImage(imageData);

        const prediction = await this.model.predict(
            preprocessedImage,
            this.TOPK_PREDICTIONS,
        );

        // const doneIn = performance.now() - startTime;

        return { url, prediction: prediction.dataSync()[0] };
    }
}

export const imageClassifier = new ImageClassifier('http://127.0.0.1:5500/v8/model.json');
