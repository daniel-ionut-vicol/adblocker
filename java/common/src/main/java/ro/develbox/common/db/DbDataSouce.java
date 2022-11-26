package ro.develbox.common.db;

import java.sql.Connection;
import java.sql.SQLException;

import org.apache.commons.dbcp2.BasicDataSource;

import ro.develbox.common.Env;

public class DbDataSouce {

	private static BasicDataSource ds = new BasicDataSource();

	static {
		ds.setUrl(Env.getDbUrl());
		ds.setUsername(Env.getDbUser());
		ds.setPassword(Env.getDbPass());
		ds.setMinIdle(Env.getDbMinConns());
		ds.setMaxIdle(Env.getDbMaxConns());
		ds.setMaxOpenPreparedStatements(Env.getDbMaxSts());
	}

	public static Connection getConnection() throws SQLException {
		return ds.getConnection();
	}

	private DbDataSouce() {
	}

}
