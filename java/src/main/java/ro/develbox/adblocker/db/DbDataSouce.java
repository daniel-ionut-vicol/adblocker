package ro.develbox.adblocker.db;

import java.sql.Connection;
import java.sql.SQLException;

import org.apache.commons.dbcp2.BasicDataSource;

public class DbDataSouce {
	private static final String DB_URL_ENV = "DB_URL";
	private static final String DB_USER = "DB_USER";
	private static final String DB_PASS = "DB_PASS";
	private static final String DB_MIN_CONN = "DB_MIN_CONN";
	private static final String DB_MAX_CONN = "DB_MAX_CONN";
	private static final String DB_MAX_STS = "DB_MAX_STS";
	
	private static BasicDataSource ds = new BasicDataSource();

	static {
		ds.setUrl(System.getenv(DB_URL_ENV));
		ds.setUsername(System.getenv(DB_USER));
		ds.setPassword(System.getenv(DB_PASS));
		ds.setMinIdle(getEnvIntPropValue(DB_MIN_CONN, 1));
		ds.setMaxIdle(getEnvIntPropValue(DB_MAX_CONN, 10));
		ds.setMaxOpenPreparedStatements(getEnvIntPropValue(DB_MAX_STS, 100));
	}

	public static Connection getConnection() throws SQLException {
		return ds.getConnection();
	}

	private DbDataSouce(){ }
	
	private static int getEnvIntPropValue(String propName, int defaultValue) {
		String envValue = System.getenv(propName);
		if(envValue==null || envValue.trim().isEmpty()) {
			return defaultValue;
		}else {
			return Integer.parseInt(envValue);
		}
	}
	
	public static void main(String[] args) throws SQLException {
		Connection conn = DbDataSouce.getConnection();
		System.out.println(conn.isClosed());
	}
}
