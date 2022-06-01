package ro.develbox.adblocker.db.model;

public class Site {
	public static final int FREE = 0;
	public static final int PROCESSING = 1;
	public static final int INVALID = 9999;

	private int id;
	private String url;
	private String cookieConfirm;
	private String closeFullPageAdd;
	private int status;
	private int maxPages;
	private int maxDepth;

	public Site() {

	}

	public Site(int id, String url, String cookieConfirm, String closeFullPageAdd, int status, int maxPages,
			int maxDepth) {
		super();
		this.id = id;
		this.url = url;
		this.cookieConfirm = cookieConfirm;
		this.closeFullPageAdd = closeFullPageAdd;
		this.status = status;
		this.maxPages = maxPages;
		this.maxDepth = maxDepth;
	}

	public int getId() {
		return id;
	}

	public void setId(int id) {
		this.id = id;
	}

	public String getUrl() {
		return url;
	}

	public void setUrl(String url) {
		this.url = url;
	}

	public String getCookieConfirm() {
		return cookieConfirm;
	}

	public void setCookieConfirm(String cookieConfirm) {
		this.cookieConfirm = cookieConfirm;
	}

	public String getCloseFullPageAdd() {
		return closeFullPageAdd;
	}

	public void setCloseFullPageAdd(String closeFullPageAdd) {
		this.closeFullPageAdd = closeFullPageAdd;
	}

	public int getStatus() {
		return status;
	}

	public void setStatus(int status) {
		this.status = status;
	}

	public int getMaxPages() {
		return maxPages;
	}

	public void setMaxPages(int maxPages) {
		this.maxPages = maxPages;
	}

	public int getMaxDepth() {
		return maxDepth;
	}

	public void setMaxDepth(int maxDepth) {
		this.maxDepth = maxDepth;
	}

}
