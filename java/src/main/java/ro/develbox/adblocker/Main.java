package ro.develbox.adblocker;

import java.io.IOException;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.URL;
import java.sql.SQLException;
import java.time.Duration;
import java.util.Date;
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

	public static void main(String[] args) throws SQLException, InterruptedException, IOException {
		//startHealthCheckServer();
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
		WebDriver driver = null;
		while (true) {
			try {
				site = siteService.getNextAndUpdateFreeSite();
				logger.debug("Selected site {}", site);
				if (site != null) {
					reportService.initializeReportRow(site.getId());
					try {
						logger.debug("Getting driver from grid {}", gridAddress);
						driver = new RemoteWebDriver(new URL(gridAddress), capabilities);
						logger.debug("Got driver from grid {}", gridAddress);
						driver.manage().timeouts().implicitlyWait(Duration.ofMillis(100));
						logger.debug("Start processing site {}", site.getUrl());
						SiteProcessorReport report = processor.processSite(driver, site);
						siteService.updateSiteStatus(site.getId(), Site.FREE);
						reportService.updateReport(site.getId(), report);
						logger.debug("Finished processing site {}, pages : {}, ads : {}, nonAds {}", site.getUrl(),
								report.getPages(), report.getAds(), report.getNonAds());
					} finally {
						if (site != null && siteService != null) {
							siteService.updateSiteStatus(site.getId(), Site.FREE);
						}
					}
				} else {
					logger.debug("No available site");
				}
			} catch (Exception e) {
				logger.error("Exception processing site", e);
			}
			finally {
				if(driver!=null) {
					try {
						driver.close();
					}catch (Exception e) {
					}
				}
				logger.debug("Sleeping for 1 minute");
				TimeUnit.MINUTES.sleep(1);
			}
		}
	}

	private static void startHealthCheckServer() throws IOException {
		final ServerSocket serverSocket = new ServerSocket(9999);
		Runtime.getRuntime().addShutdownHook(new Thread() {
			public void run() {
				try {
					if (serverSocket != null) {
						serverSocket.close();
					}
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
			};
		});
		new Thread() {
			public void run() {
				try {
					while (true) {
						Socket socket = serverSocket.accept();
						OutputStream output = socket.getOutputStream();
						PrintWriter writer = new PrintWriter(output, true);

						writer.println(new Date().toString());
						socket.close();
					}
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}

			};
		}.start();
	}
}
