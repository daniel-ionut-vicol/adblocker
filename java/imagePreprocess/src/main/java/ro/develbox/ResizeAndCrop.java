package ro.develbox;

import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import javax.imageio.ImageIO;

public class ResizeAndCrop {
	public static void main(String[] args) {
		try {
			File input = new File("input.jpg");
			BufferedImage image = ImageIO.read(input);

			int width = 224; // desired width of the image
			int height = 224; // desired height of the image
			int x = (image.getWidth() - width) / 2; // calculate x-coordinate for cropping
			int y = (image.getHeight() - height) / 2; // calculate y-coordinate for cropping

			// Crop the image
			BufferedImage croppedImage = image.getSubimage(x, y, width, height);

			// Resize the image
			BufferedImage resizedImage = new BufferedImage(224, 224, BufferedImage.TYPE_INT_RGB);
			resizedImage.createGraphics().drawImage(croppedImage, 0, 0, 224, 224, null);

			// Save the output image
			File output = new File("output.jpg");
			ImageIO.write(resizedImage, "jpg", output);
		} catch (IOException ex) {
			System.out.println("Error processing image: " + ex.getMessage());
		}
	}
}
