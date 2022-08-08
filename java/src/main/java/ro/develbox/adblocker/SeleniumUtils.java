package ro.develbox.adblocker;

import java.time.Duration;
import java.util.concurrent.TimeUnit;

import org.openqa.selenium.Alert;
import org.openqa.selenium.By;
import org.openqa.selenium.ElementClickInterceptedException;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import ro.develbox.adblocker.db.model.Site;

public class SeleniumUtils {

	private static Logger logger = LoggerFactory.getLogger(SeleniumUtils.class);

	public static void closeAnnoyingElements(WebDriver webDriver, Site site, boolean waitElements) {
		// check if alert present and dismiss it
		try {
			Alert alert = webDriver.switchTo().alert();
			alert.dismiss();
		} catch (Exception e) {

		}
		// close any annoying think on the page
		if (site.getAnnoyingPageElements() != null) {
			for (String element : site.getAnnoyingPageElements()) {
				logger.debug("Trying to close annoying element {}" , element);
				try {
					if (waitElements) {
						WebDriverWait wait = new WebDriverWait(webDriver, Duration.ofSeconds(60),
								Duration.ofSeconds(1));
						wait.until(ExpectedConditions.presenceOfElementLocated(By.xpath(element)));
					}else {
						//if we try and get the element we'll use the default wait time 
						WebDriverWait wait = new WebDriverWait(webDriver, Duration.ofMillis(20),
								Duration.ofMillis(10));
						wait.until(ExpectedConditions.presenceOfElementLocated(By.xpath(element)));
					}
					WebElement closeFullPageAddElement = webDriver.findElement(By.xpath(element));
					SeleniumUtils.scrollToElement(webDriver, closeFullPageAddElement);
					closeFullPageAddElement.click();
					logger.debug("Annoying element {} closed from page {}" , element, webDriver.getCurrentUrl());
				} catch (Exception e) {
					logger.debug("Annoying element {} not found on page" , element);
				}
			}
		}else {
			logger.debug("No annoying elements config for site {}", site.getUrl());
		}
	}

	public static void click(WebDriver webDriver, Site site, WebElement element) {
		try {
			SeleniumUtils.scrollToElement(webDriver, element);
			element.click();
		}catch (ElementClickInterceptedException e) {
			SeleniumUtils.closeAnnoyingElements(null, null, false);
			element.click();
		}
	}
	
	public static void scrollToElement(WebDriver webDriver, WebElement element) {
		try {
			((JavascriptExecutor) webDriver).executeScript(
					"arguments[0].scrollIntoView({\r\n" + "            behavior: 'auto',\r\n"
							+ "            block: 'center',\r\n" + "            inline: 'center'\r\n" + "        });",
					element);
			TimeUnit.SECONDS.sleep(1);
		} catch (Exception e) {
			logger.error("Exception scrolling to element", e);
		}
	}

	public static void randomWait() {
		long wait = (long) (Math.random() * 10);
		logger.debug("Random wait for {} seconds", wait);
		try {
			TimeUnit.SECONDS.sleep(wait);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
