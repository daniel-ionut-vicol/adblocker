package ro.develbox.adblocker;

import org.openqa.selenium.WebDriver;

import ro.develbox.adblocker.db.model.Site;

public interface PageInfoExtractor<T> {
	public int extractPageInfo(WebDriver webDriver, Site site);
}
