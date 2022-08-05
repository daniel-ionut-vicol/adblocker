package ro.develbox.adblocker.db.service;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

import ro.develbox.adblocker.SiteProcessorReport;
import ro.develbox.adblocker.db.DbDataSouce;

public class ReportService {

	public void updateReport(int siteId, SiteProcessorReport report) throws SQLException {
		try (Connection conn = DbDataSouce.getConnection()) {
			try (PreparedStatement ps = conn.prepareStatement(
					"UPDATE site_report set pages_visited = pages_visited + ?, ads_no = ads_no + ? where id=?")) {
				ps.setInt(1, report.getPages());
				ps.setInt(2, report.getAds());
				ps.setInt(3, siteId);
				ps.executeUpdate();
			}
		}
	}
}
