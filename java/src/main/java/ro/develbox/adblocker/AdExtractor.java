package ro.develbox.adblocker;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.nio.file.Files;
import java.time.Duration;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.concurrent.TimeUnit;

import org.openqa.selenium.By;
import org.openqa.selenium.Dimension;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.OutputType;
import org.openqa.selenium.TakesScreenshot;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebDriverException;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.interactions.Actions;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class AdExtractor {

	private static final String ADS_FILE_PATH_ENV = "ADS_DIR";
	private static final String ADS_FILE_PATH_ENV_DEF = "./ads/";
	private static String ADS_FILE_PATH;
	
	private static final String[] adsXpath = new String[] { "//*[@data-google-query-id]" };

	private static Logger logger = LoggerFactory.getLogger(AdExtractor.class);

	public int extractPageAds(WebDriver webDriver) {
		WebDriverWait wait = new WebDriverWait(webDriver, Duration.ofSeconds(10), Duration.ofMillis(100));
		List<WebElement> ads = new ArrayList<>();
		int totalAds = 0 ;
		for (String adXpath : adsXpath) {
			try {
				ads.addAll(getAdsElements(webDriver, adXpath));
			} catch (Exception e) {
				logger.error("Exception getting ads by " + adXpath);
			}
		}
		for (WebElement ad : ads) {
			try {
				if(ad.isDisplayed()) {
					((JavascriptExecutor) webDriver).executeScript("arguments[0].scrollIntoView({\r\n"
							+ "            behavior: 'auto',\r\n"
							+ "            block: 'center',\r\n"
							+ "            inline: 'center'\r\n"
							+ "        });", ad);
					wait.until(ExpectedConditions.visibilityOf(ad));
					TimeUnit.SECONDS.sleep(1);
//					actions.moveToElement(ad).perform();
					byte [] bytes = ad.getScreenshotAs(OutputType.BYTES);
					int hashCode = Arrays.hashCode(bytes);
					String paddedHash = String.format("%012d", hashCode);
					String[] dirparts = paddedHash.split("(?<=\\G.{3})");
					String dirs = String.join("/", dirparts);
					File directory = new File(AdExtractor.getAdspath()+dirs);
					if(!directory.exists()) {
						directory.mkdirs();
					}
					String imageFile = paddedHash + ".png";
					try (FileOutputStream outputStream = new FileOutputStream(directory.getAbsolutePath() + "/" + imageFile)) {
					    outputStream.write(bytes);
					}
					String htmlFile = paddedHash + ".html";
					try (FileOutputStream outputStream = new FileOutputStream(directory.getAbsolutePath() + "/" + htmlFile)) {
					    outputStream.write(ad.getAttribute("innerHTML").getBytes("UTF-8"));
					}
					totalAds++;
				}
				
			}catch (Exception e) {
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
	
	private static String getAdspath () {
		if(ADS_FILE_PATH==null) {
			String envVal = System.getenv(ADS_FILE_PATH_ENV);
			if(envVal== null || envVal.trim().isEmpty()) {
				envVal = ADS_FILE_PATH_ENV_DEF;
			}
			ADS_FILE_PATH = envVal;
		}
		return ADS_FILE_PATH;
	}
}
