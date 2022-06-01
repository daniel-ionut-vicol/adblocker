package ro.develbox.adblocker.db.service;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Timestamp;
import java.util.concurrent.TimeUnit;

import ro.develbox.adblocker.db.DbDataSouce;
import ro.develbox.adblocker.db.model.Site;

public class SiteService {

	public Site getNextAndUpdateFreeSite() throws SQLException {
		try (Connection conn = DbDataSouce.getConnection()) {
			try (PreparedStatement ps = conn
					.prepareStatement("SELECT * from site where status = ? or update_time < ?")) {
				ps.setInt(1, Site.FREE);
				ps.setTimestamp(2, new Timestamp(System.currentTimeMillis() - TimeUnit.HOURS.toMillis(1)));
				try (ResultSet rs = ps.executeQuery()) {
					if (rs.next()) {
						Site site = new Site(rs.getInt("id"), rs.getString("url"), rs.getString("cookie_confirm"),
								rs.getString("close_page_ad"), rs.getInt("status"), rs.getInt("max_pages"),
								rs.getInt("max_depth"));
						updateSiteStatus(conn, site.getId(), Site.PROCESSING);
						return site;
					}
				}
			}
		}
		return null;
	}

	public void updateSiteStatus(int siteId, int status) throws SQLException {
		try (Connection conn = DbDataSouce.getConnection()) {
			updateSiteStatus(conn, siteId, status);
		}
	}

	private void updateSiteStatus(Connection conn, int siteId, int status) throws SQLException {
		try (PreparedStatement ps = conn.prepareStatement("UPDATE site set status =  ? where id = ?")) {
			ps.setInt(1, status);
			ps.setInt(2, siteId);
			ps.executeUpdate();
		}
	}
}
