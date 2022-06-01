package ro.develbox.adblocker;

import java.util.Collections;
import java.util.List;
import java.util.Set;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class LinksExtractor {
	private static Logger logger = LoggerFactory.getLogger(SiteProcessor.class);

	public List<WebElement> extractLinks(WebDriver driver, String baseLink) {
		List<WebElement> links = driver.findElements(By.tagName("a"));
		return links;
	}

	public WebElement chooseRandomLink(WebDriver driver, Set<String> excluded, String baseLink) {
		List<WebElement> links = extractLinks(driver, baseLink);
		Collections.shuffle(links);
		for (WebElement link : links) {
			try {
				if (link.isDisplayed()) {
					String actualLink = getElementLink(link);
					// TODO maybe we should also check relative link ????
					if (actualLink != null && !excluded.contains(actualLink) && actualLink.contains(baseLink)) {
						excluded.add(actualLink);
						logger.debug("Choosed link that goes to {}", actualLink);
						return link;
					}
				}
			} catch (Exception e) {
				logger.error("Exception ay random link ", e);
			}
		}
		logger.debug("No link choosed");
		return null;
	}

	private String getElementLink(WebElement element) {
		String actualLink = element.getAttribute("href");
		return actualLink;
	}
}
