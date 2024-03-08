package ro.develbox.adblocker;

import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.URL;
import java.time.Duration;
import java.util.List;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import ro.develbox.common.Env;
import ro.develbox.common.db.model.Site;

public class AdExtractor implements PageInfoExtractor {

    private static Logger logger = LoggerFactory.getLogger(AdExtractor.class);

    @Override
    public int extractPageInfo(WebDriver webDriver, Site site) {
        return extractPageAds(webDriver, site);
    }

    public int extractPageAds(WebDriver webDriver, Site site) {
        logger.debug("Getting ads from page {}", webDriver.getCurrentUrl()); // use logger.debug() for low-level

        WebDriverWait wait = new WebDriverWait(webDriver, Duration.ofSeconds(10));

        try {
            // Find all iframes
            List<WebElement> iframes = webDriver.findElements(By.tagName("iframe"));
            logger.info("Found {} iframes", iframes.size()); // use logger.info() for general messages

            // Switch to each iframe and check the content
            for (WebElement iframe : iframes) {
                wait.until(ExpectedConditions.frameToBeAvailableAndSwitchToIt(iframe));

                String iframeSource = webDriver.getPageSource();
                if (iframeSource.isEmpty()) {
                    logger.debug("The iframe is empty"); // use logger.warn() for potential issues
                } else {
                    logger.debug("The iframe has contents");
                    logger.debug(iframeSource);

                    // Find all images within the iframe
                    List<WebElement> images = webDriver.findElements(By.tagName("img"));
                    logger.debug("Found {} images", images.size());

                    // Filter and process the images
                    for (WebElement image : images) {
                        // Check if the image is valid
                        int imageHeight = Integer.parseInt(image.getAttribute("naturalHeight"));
                        int imageWidth = Integer.parseInt(image.getAttribute("naturalWidth"));
                        if (imageHeight > 100 && imageWidth > 100) {
                            // Get the image source
                            String imageSource = image.getAttribute("src");
                            logger.debug("Valid Image Source: {}", imageSource);

                            // Save the image
                            saveImage(imageSource, site);
                        }
                    }
                }

                webDriver.switchTo().defaultContent(); // switch back to the main content
            }

            return iframes.size();
        } catch (Exception e) {
            logger.error("Exception getting ads using Selenium", e);
            return 0;
        }
    }

    // Save image to the specified directory
    private void saveImage(String imageUrl, Site site) {
        try {
            URL url = new URL(imageUrl);

            // Create the directory structure based on the URL hash
            int hashCode = url.toString().hashCode();
            String paddedHash = String.format("%012d", hashCode);
            String[] dirParts = paddedHash.split("(?<=\\G.{3})");
            String dirs = String.join(File.separator, dirParts);
            File directory = new File(Env.getAdspath() + dirs);
            if (!directory.exists()) {
                directory.mkdirs();
            }

            // Extract the image file name from the URL
            String imageName = paddedHash + ".png";
            File imageFile = new File(directory.getAbsolutePath() + File.separator + imageName);

            // Open a stream to the image URL and save the image
            try (InputStream inputStream = url.openStream();
                    FileOutputStream outputStream = new FileOutputStream(imageFile)) {
                byte[] buffer = new byte[1024];
                int bytesRead;
                while ((bytesRead = inputStream.read(buffer)) != -1) {
                    outputStream.write(buffer, 0, bytesRead);
                }

                logger.debug("Image saved to: {}", imageFile.getAbsolutePath());
            }
        } catch (IOException e) {
            logger.error("Exception saving image", e);
        }
    }
}
