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
	
	public void initializeReportRow(int siteId) throws SQLException{
		try (Connection conn = DbDataSouce.getConnection()) {
			try (PreparedStatement ps = conn.prepareStatement(
					"INSERT IGNORE INTO site_report set id= ? , pages_visited = 0 , ads_no = 0")) {
				ps.setInt(1, siteId);
				ps.executeUpdate();
			}
		}
	}
}
