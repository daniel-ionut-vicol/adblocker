package ro.develbox.adblocker;

import java.time.Duration;
import java.util.HashSet;
import java.util.Set;
import java.util.concurrent.TimeUnit;

import org.openqa.selenium.By;
import org.openqa.selenium.JavascriptExecutor;
import org.openqa.selenium.NoSuchElementException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import ro.develbox.adblocker.db.model.Site;

public class SiteProcessor {

	private static Logger logger = LoggerFactory.getLogger(SiteProcessor.class);

	private AdExtractor adExtractor = new AdExtractor();
	private LinksExtractor linksExtractor = new LinksExtractor();

	public SiteProcessorReport processSite(WebDriver webDriver, Site site) {
		SiteProcessorReport reportResult = new SiteProcessorReport();
		try {
			Set<String> visited = new HashSet<>();
			visited.add(site.getUrl());
			webDriver.get(site.getUrl());
			if (site.getCookieConfirm() != null && !site.getCookieConfirm().trim().isEmpty()) {
				try {
					WebDriverWait wait = new WebDriverWait(webDriver, Duration.ofSeconds(10),Duration.ofSeconds(1));
					wait.until(ExpectedConditions.presenceOfElementLocated(By.xpath(site.getCookieConfirm())));
					WebElement cookieCnfirm = webDriver.findElement(By.xpath(site.getCookieConfirm()));
					cookieCnfirm.click();
					logger.debug("Confirmed cookies for site {}", site.getUrl());
				} catch (NoSuchElementException e) {
					logger.debug("Cookie confirm not present on page for site {}", site.getUrl());
				}
			}
			visit(webDriver, site, reportResult, 0, visited);
		} catch (Exception e) {
			logger.error("Processing site " + site.getUrl() + " exception ", e);
		}
		return reportResult;
	}

	private void visit(WebDriver webDriver,  Site site, SiteProcessorReport reportResult, int curentDepth,
			Set<String> visited) {
		randomWait();
		if(site.getCloseFullPageAdd()!=null) {
			try {
				WebElement closeFullPageAddElement = webDriver.findElement(By.xpath(site.getCloseFullPageAdd()));
				((JavascriptExecutor) webDriver).executeScript("arguments[0].scrollIntoView({\r\n"
						+ "            behavior: 'auto',\r\n"
						+ "            block: 'center',\r\n"
						+ "            inline: 'center'\r\n"
						+ "        });", closeFullPageAddElement);
				closeFullPageAddElement.click();
			}catch (Exception e) {
			}
		}
		logger.debug("Visiting page {}", webDriver.getCurrentUrl());
		int ads = adExtractor.extractPageAds(webDriver);
		reportResult.incrementAds(ads);
		reportResult.incrementPages(1);

		while (true) {
			// get next random link from page
			WebElement link = linksExtractor.chooseRandomLink(webDriver, visited, site.getUrl());
			//should we go deeper in the page
			boolean goDeeper = (curentDepth < site.getMaxDepth() && (Math.random() < 0.5)) || curentDepth == 0;
			if (link!=null && goDeeper) {
				logger.debug("Elected to go deeper on site {}", site.getUrl());
				try {
					((JavascriptExecutor) webDriver).executeScript("arguments[0].scrollIntoView({\r\n"
							+ "            behavior: 'auto',\r\n"
							+ "            block: 'center',\r\n"
							+ "            inline: 'center'\r\n"
							+ "        });", link);
					link.click();
				}catch (Exception e) {
					logger.error("Exception using link to navigate will try next link " , e);
					continue;
				}
				visit(webDriver, site, reportResult, curentDepth + 1, visited);
			} else {
				// go back to previous page
				webDriver.navigate().back();
				return;
			}
		}

	}
	
	private void randomWait() {
		long wait = (long)(Math.random() * 10);
		logger.debug("Random wait for {} seconds" , wait);
		try {
			TimeUnit.SECONDS.sleep(wait);
		} catch (InterruptedException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
