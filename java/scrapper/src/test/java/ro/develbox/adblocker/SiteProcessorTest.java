package ro.develbox.adblocker;

import java.net.MalformedURLException;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;

import org.junit.jupiter.api.Test;
import org.openqa.selenium.PersistentCapabilities;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.remote.RemoteWebDriver;

import ro.develbox.common.db.model.Site;

public class SiteProcessorTest {

	@Test
	public void testSiteProcessing() throws MalformedURLException {
		PersistentCapabilities capabilities = new PersistentCapabilities();
		WebDriver driver = new RemoteWebDriver(new URL("http://localhost:9515"), capabilities);
		SiteProcessor processor = new  SiteProcessor();
		Site site = new Site();
		site.setUrl("https://www.sport.ro/");
		List<String> annoyingPageElements = new ArrayList<>();
		annoyingPageElements.add("//*[@id=\"onetrust-accept-btn-handler\"]");
		annoyingPageElements.add("//*[@id=\"onesignal-slidedown-cancel-button\"]");
		annoyingPageElements.add("//*[@id=\"byebyevideo\"]");
		site.setAnnoyingPageElements(annoyingPageElements);
		site.setMaxDepth(1);
		site.setMaxPages(1);
		site.setMaxNonAdImgs(2);
		SiteProcessorReport report = processor.processSite(driver, site);
		System.out.println(report.getPages());
		System.out.println(report.getAds());
		System.out.println(report.getNonAds());
		driver.close();
	}
}
