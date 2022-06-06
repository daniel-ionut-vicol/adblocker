package ro.develbox.adblocker;

import java.time.Duration;
import java.util.concurrent.TimeUnit;

import org.openqa.selenium.Alert;
import org.openqa.selenium.By;
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
				try {
					if (waitElements) {
						WebDriverWait wait = new WebDriverWait(webDriver, Duration.ofSeconds(10),
								Duration.ofSeconds(1));
						wait.until(ExpectedConditions.presenceOfElementLocated(By.xpath(element)));
					}
					WebElement closeFullPageAddElement = webDriver.findElement(By.xpath(element));
					SeleniumUtils.scrollToElement(webDriver, closeFullPageAddElement);
					closeFullPageAddElement.click();
				} catch (Exception e) {
				}
			}
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
