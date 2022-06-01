package ro.develbox.adblocker;

import java.net.MalformedURLException;
import java.net.URL;

import org.junit.jupiter.api.Test;
import org.openqa.selenium.PersistentCapabilities;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.remote.RemoteWebDriver;

import ro.develbox.adblocker.db.model.Site;

public class SiteProcessorTest {

	@Test
	public void testSiteProcessing() throws MalformedURLException {
		PersistentCapabilities capabilities = new PersistentCapabilities();
		WebDriver driver = new RemoteWebDriver(new URL("http://localhost:9515"), capabilities);
		SiteProcessor processor = new  SiteProcessor();
		Site site = new Site();
		site.setUrl("https://www.sport.ro/");
		site.setCookieConfirm("//*[@id=\"onetrust-accept-btn-handler\"]");
		site.setMaxDepth(4);
		site.setMaxPages(50);
		SiteProcessorReport report = processor.processSite(driver, site);
		System.out.println(report.getPages());
		System.out.println(report.getAds());
		driver.close();
	}
}
