package ro.develbox.adblocker.db.model;

import java.util.List;

public class Site {
	public static final int FREE = 0;
	public static final int PROCESSING = 1;
	public static final int INVALID = 9999;

	private int id;
	private String url;
	private List<String> annoyingPageElements ;
	private int status;
	private int maxPages;
	private int maxDepth;

	public Site() {

	}

	public Site(int id, String url, List<String> annoyingPageElements, int status, int maxPages,
			int maxDepth) {
		super();
		this.id = id;
		this.url = url;
		this.annoyingPageElements = annoyingPageElements;
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

	public List<String> getAnnoyingPageElements() {
		return this.annoyingPageElements;
	}

	public void setAnnoyingPageElements(List<String> annoyingPageElements) {
		this.annoyingPageElements = annoyingPageElements;
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
