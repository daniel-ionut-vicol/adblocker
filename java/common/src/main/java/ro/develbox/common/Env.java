package ro.develbox.common;

public class Env {
	private static final String DB_URL_ENV = "DB_URL";
	private static final String DB_USER = "DB_USER";
	private static final String DB_PASS = "DB_PASS";
	private static final String DB_MIN_CONN = "DB_MIN_CONN";
	private static final String DB_MAX_CONN = "DB_MAX_CONN";
	private static final String DB_MAX_STS = "DB_MAX_STS";

	public static String getDbUrl() {
		return System.getenv(DB_URL_ENV);
	}

	public static String getDbUser() {
		return System.getenv(DB_USER);
	}

	public static String getDbPass() {
		return System.getenv(DB_PASS);
	}

	public static int getDbMinConns() {
		return getEnvIntPropValue(DB_MIN_CONN, 1);
	}

	public static int getDbMaxConns() {
		return getEnvIntPropValue(DB_MAX_CONN, 10);
	}

	public static int getDbMaxSts() {
		return getEnvIntPropValue(DB_MAX_STS, 100);
	}

	public static int getEnvIntPropValue(String propName, int defaultValue) {
		String envValue = System.getenv(propName);
		if (envValue == null || envValue.trim().isEmpty()) {
			return defaultValue;
		} else {
			return Integer.parseInt(envValue);
		}
	}

	private static final String ADS_FILE_PATH_ENV = "ADS_DIR";
	private static final String ADS_FILE_PATH_ENV_DEF = "./ads/";
	private static String ADS_FILE_PATH;

	public static String getAdspath() {
		if (ADS_FILE_PATH == null) {
			String envVal = System.getenv(ADS_FILE_PATH_ENV);
			if (envVal == null || envVal.trim().isEmpty()) {
				envVal = ADS_FILE_PATH_ENV_DEF;
			}
			ADS_FILE_PATH = envVal;
		}
		return ADS_FILE_PATH;
	}

	private static final String NON_ADS_FILE_PATH_ENV = "NON_ADS_DIR";
	private static final String NON_ADS_FILE_PATH_ENV_DEF = "./nonAds/";
	private static String NON_ADS_FILE_PATH;

	public static String getNonAdspath() {
		if (NON_ADS_FILE_PATH == null) {
			String envVal = System.getenv(NON_ADS_FILE_PATH_ENV);
			if (envVal == null || envVal.trim().isEmpty()) {
				envVal = NON_ADS_FILE_PATH_ENV_DEF;
			}
			NON_ADS_FILE_PATH = envVal;
		}
		return NON_ADS_FILE_PATH;
	}

	private static String GRID_ENV = "GRID_ADDRESS";
	private static String GRID_DEF = "http://192.168.69.207:4444";

	public static String getSeleniumGridAddress() {
		String gridAddress = System.getenv(GRID_ENV);
		if (gridAddress == null || gridAddress.trim().isEmpty()) {
			gridAddress = GRID_DEF;
		}
		return gridAddress;
	}

}
