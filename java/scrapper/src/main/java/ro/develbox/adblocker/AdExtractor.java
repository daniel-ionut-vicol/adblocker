package ro.develbox.adblocker;

import java.io.File;
import java.io.FileOutputStream;
import java.time.Duration;
import java.util.ArrayList;
import java.util.Arrays;
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

public class AdExtractor implements PageInfoExtractor{

	private static final String[] adsXpath = new String[] { "//*[@data-google-query-id]" };

	private static Logger logger = LoggerFactory.getLogger(AdExtractor.class);

	@Override
	public int extractPageInfo(WebDriver webDriver, Site site) {
		return extractPageAds(webDriver, site);
	}
	
	public int extractPageAds(WebDriver webDriver, Site site) {
		logger.debug("Getting ads from page {}" , webDriver.getCurrentUrl());
		WebDriverWait wait = new WebDriverWait(webDriver, Duration.ofSeconds(10), Duration.ofMillis(100));
		List<WebElement> ads = new ArrayList<>();
		int totalAds = 0;
		for (String adXpath : adsXpath) {
			try {
				ads.addAll(getAdsElements(webDriver, adXpath));
				logger.debug("Extracted {} ads elements" , ads.size());
			} catch (Exception e) {
				logger.error("Exception getting ads by " + adXpath);
			}
		}
		for (WebElement ad : ads) {
			SeleniumUtils.closeAnnoyingElements(webDriver, site, false);
			try {
				if (ad.isDisplayed()) {
					SeleniumUtils.scrollToElement(webDriver, ad);
					wait.until(ExpectedConditions.visibilityOf(ad));
					TimeUnit.SECONDS.sleep(1);
//					actions.moveToElement(ad).perform();
					byte[] bytes = ad.getScreenshotAs(OutputType.BYTES);
					int hashCode = Arrays.hashCode(bytes);
					String paddedHash = String.format("%012d", hashCode);
					String[] dirparts = paddedHash.split("(?<=\\G.{3})");
					String dirs = String.join("/", dirparts);
					File directory = new File(Env.getAdspath() + dirs);
					if (!directory.exists()) {
						directory.mkdirs();
					}
					String imageFile = paddedHash + ".png";
					logger.debug("Saving addFile {} in directory {}" , imageFile, directory.getAbsolutePath());
					try (FileOutputStream outputStream = new FileOutputStream(
							directory.getAbsolutePath() + "/" + imageFile)) {
						outputStream.write(bytes);
					}
					String htmlFile = paddedHash + ".html";
					try (FileOutputStream outputStream = new FileOutputStream(
							directory.getAbsolutePath() + "/" + htmlFile)) {
						outputStream.write(ad.getAttribute("innerHTML").getBytes("UTF-8"));
					}
					totalAds++;
				}else {
					logger.error("Ad not displayed {}" , ad);
				}

			} catch (Exception e) {
				e.printStackTrace();
				logger.error("Exception getting ads image");
			}
		}
		return totalAds;
	}

	// find elements with data-google-query-id attribute
	public List<WebElement> getAdsElements(WebDriver webDriver, String xpath) {
		return webDriver.findElements(By.xpath(xpath));
	}

}