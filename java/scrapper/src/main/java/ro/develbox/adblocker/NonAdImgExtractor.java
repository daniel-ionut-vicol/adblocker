package ro.develbox.adblocker;

import java.io.File;
import java.io.FileOutputStream;
import java.net.URI;
import java.net.URISyntaxException;
import java.time.Duration;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.concurrent.TimeUnit;

import org.openqa.selenium.By;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import ro.develbox.common.Env;
import ro.develbox.common.db.model.Site;

public class NonAdImgExtractor implements PageInfoExtractor{
	
	private static Logger logger = LoggerFactory.getLogger(NonAdImgExtractor.class);

	@Override
	public int extractPageInfo(WebDriver webDriver, Site site) {
		return extractPageImages(webDriver, site);
	}
	
	public int extractPageImages(WebDriver webDriver, Site site) {
		logger.debug("Getting non ads images from page {}" , webDriver.getCurrentUrl());
		WebDriverWait wait = new WebDriverWait(webDriver, Duration.ofSeconds(10), Duration.ofMillis(100));
		List<WebElement> images = new ArrayList<>();
		int totalImgs = 0;
		String domain;
		try {
			domain = new URI(site.getUrl()).getHost();
			if(domain.startsWith("www.")) {
				domain= domain.substring(4);
			}
		} catch (URISyntaxException e1) {
			e1.printStackTrace();
			return 0 ;
		}
		String imgXpath = "//img[contains(@src,'"+domain+"')]";
		try {
			images.addAll( webDriver.findElements(By.xpath(imgXpath)));
			logger.debug("Extracted {} images elements" , images.size());
		} catch (Exception e) {
			logger.error("Exception getting images by " + imgXpath);
		}
		//randomize the list so we do not always get the same images on the same page 
		Collections.shuffle(images);

		for (WebElement img : images) {
			if(totalImgs>site.getMaxNonAdImgs()) {
				break;
			}
			SeleniumUtils.closeAnnoyingElements(webDriver, site, false);
			try {
				if (img.isDisplayed()) {
					SeleniumUtils.scrollToElement(webDriver, img);
					wait.until(ExpectedConditions.visibilityOf(img));
					TimeUnit.SECONDS.sleep(1);
//					actions.moveToElement(ad).perform();
					byte[] bytes = img.getScreenshotAs(OutputType.BYTES);
					int hashCode = Arrays.hashCode(bytes);
					String paddedHash = String.format("%012d", hashCode);
					String[] dirparts = paddedHash.split("(?<=\\G.{3})");
					String dirs = String.join("/", dirparts);
					File directory = new File(Env.getNonAdspath() + dirs);
					if (!directory.exists()) {
						directory.mkdirs();
					}
					String imageFile = paddedHash + ".png";
					logger.debug("Saving nonaddFile {} in directory {}" , imageFile, directory.getAbsolutePath());
					try (FileOutputStream outputStream = new FileOutputStream(
							directory.getAbsolutePath() + "/" + imageFile)) {
						outputStream.write(bytes);
					}
					String htmlFile = paddedHash + ".html";
					try (FileOutputStream outputStream = new FileOutputStream(
							directory.getAbsolutePath() + "/" + htmlFile)) {
						outputStream.write(img.getAttribute("innerHTML").getBytes("UTF-8"));
					}
					totalImgs++;
				}else {
					logger.error("NonAd not displayed {}" , img);
				}

			} catch (Exception e) {
				e.printStackTrace();
				logger.error("Exception getting nonads image");
			}
		}
		return totalImgs;
	}

	
}
