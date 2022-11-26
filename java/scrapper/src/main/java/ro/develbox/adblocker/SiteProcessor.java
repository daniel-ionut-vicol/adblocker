package ro.develbox.adblocker;

import java.util.HashSet;
import java.util.Set;

import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import ro.develbox.common.db.model.Site;

public class SiteProcessor {

	private static Logger logger = LoggerFactory.getLogger(SiteProcessor.class);

	private AdExtractor adExtractor = new AdExtractor();
	private NonAdImgExtractor imgExtractor = new NonAdImgExtractor();
	private LinksExtractor linksExtractor = new LinksExtractor();

	public SiteProcessorReport processSite(WebDriver webDriver, Site site) {
		SiteProcessorReport reportResult = new SiteProcessorReport();
		try {
			Set<String> visited = new HashSet<>();
			visited.add(site.getUrl());
			webDriver.get(site.getUrl());
			SeleniumUtils.closeAnnoyingElements(webDriver, site, true);
			visit(webDriver, site, reportResult, 0, visited);
		} catch (Exception e) {
			logger.error("Processing site " + site.getUrl() + " exception ", e);
		}
		return reportResult;
	}

	private void visit(WebDriver webDriver, Site site, SiteProcessorReport reportResult, int curentDepth,
			Set<String> visited) {
		SeleniumUtils.randomWait();
		SeleniumUtils.closeAnnoyingElements(webDriver, site, false);
		logger.debug("Visiting page {}", webDriver.getCurrentUrl());
		int ads = adExtractor.extractPageInfo(webDriver, site);
		int nonAds = imgExtractor.extractPageInfo(webDriver, site);
		reportResult.incrementAds(ads);
		reportResult.incrementNonAds(nonAds);
		reportResult.incrementPages(1);
		if (reportResult.getPages() <= site.getMaxPages()) {
			while (true) {
				if (reportResult.getPages() <= site.getMaxPages()) {
					SeleniumUtils.closeAnnoyingElements(webDriver, site, false);
					// get next random link from page
					WebElement link = linksExtractor.chooseRandomLink(webDriver, visited, site.getUrl());
					// should we go deeper in the page
					boolean goDeeper = (curentDepth < site.getMaxDepth() && (Math.random() < 0.5)) || curentDepth == 0;
					goDeeper = goDeeper && reportResult.getPages() <= site.getMaxPages();
					if (link != null && goDeeper) {
						logger.debug("Elected to go deeper on site {}", site.getUrl());
						try {
							SeleniumUtils.click(webDriver, site, link);
						} catch (Exception e) {
							logger.error("Exception using link to navigate will try next link ", e);
							continue;
						}
						visit(webDriver, site, reportResult, curentDepth + 1, visited);
					} else {
						// go back to previous page
						webDriver.navigate().back();
						return;
					}
				} else {
					// go back to previous page
					webDriver.navigate().back();
					return;
				}
			}
		} else {
			// go back to previous page
			webDriver.navigate().back();
			return;
		}

	}

}
