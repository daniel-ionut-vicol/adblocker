package ro.develbox.adblocker;

import java.net.MalformedURLException;
import java.net.URL;
import java.sql.SQLException;
import java.util.concurrent.TimeUnit;

import org.openqa.selenium.PersistentCapabilities;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.remote.RemoteWebDriver;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import ro.develbox.adblocker.db.model.Site;
import ro.develbox.adblocker.db.service.ReportService;
import ro.develbox.adblocker.db.service.SiteService;

public class Main {

	private static Logger logger = LoggerFactory.getLogger(Main.class);

	private static String GRID_ENV = "GRID_ADDRESS";
	private static String GRID_DEF = "http://192.168.69.230:4444";

	//ISSUES :
	// dialog for notification 
	// top page add is not ok 
	public static void main(String[] args) throws MalformedURLException, SQLException, InterruptedException {
		String gridAddress = System.getenv(GRID_ENV);
		if (gridAddress == null || gridAddress.trim().isEmpty()) {
			gridAddress = GRID_DEF;
		}
		logger.debug("Using grid {}", gridAddress);
		PersistentCapabilities capabilities = new PersistentCapabilities();
		SiteProcessor processor = new SiteProcessor();
		SiteService siteService = new SiteService();
		ReportService reportService = new ReportService();
		Site site = null;
		while (true) {
			try {
				WebDriver driver = new RemoteWebDriver(new URL(gridAddress), capabilities);
				driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
				site = siteService.getNextAndUpdateFreeSite();
				if (site != null) {
					try {
						logger.debug("Start processing site {}", site.getUrl());
						SiteProcessorReport report = processor.processSite(driver, site);
						siteService.updateSiteStatus(site.getId(), Site.FREE);
						reportService.updateResport(site.getId(), report);
						logger.debug("Finished processing site {}, pages : {}, ads : {}", site.getUrl(),
								report.getPages(), report.getAds());
					} finally {
						if (site != null && siteService != null) {
							siteService.updateSiteStatus(site.getId(), Site.FREE);
						}
					}
				} else {
					logger.debug("No available site sleeping for 1 min");
					TimeUnit.MINUTES.sleep(1);
				}
				driver.close();
			} catch (Exception e) {
				logger.error("Exception sleeping for 1 min", e);
				TimeUnit.MINUTES.sleep(1);
			}
		}
	}
}
