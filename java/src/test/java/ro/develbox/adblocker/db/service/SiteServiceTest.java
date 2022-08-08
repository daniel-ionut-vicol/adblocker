package ro.develbox.adblocker.db.service;

import java.sql.SQLException;

import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import ro.develbox.adblocker.db.model.Site;

public class SiteServiceTest {

	//@Test
	public void testGetAndUpdate() throws SQLException {
		SiteService siteService = new SiteService();
		Site site = siteService.getNextAndUpdateFreeSite();
		Assertions.assertNotNull(site);
		Site site2 = siteService.getNextAndUpdateFreeSite();
		Assertions.assertTrue(site2 == null || site2.getId() != site.getId());
		siteService.updateSiteStatus(site.getId(), Site.FREE);
	}
}
