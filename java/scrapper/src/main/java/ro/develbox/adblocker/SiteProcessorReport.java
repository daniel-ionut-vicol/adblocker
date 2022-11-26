package ro.develbox.adblocker;

public class SiteProcessorReport {
	private int pages;
	private int ads;
	private int nonAds;

	public int getPages() {
		return pages;
	}

	public void incrementPages(int pages) {
		this.pages = this.pages + pages;
	}

	public int getAds() {
		return ads;
	}

	public void incrementAds(int ads) {
		this.ads = this.ads + ads;
	}

	public int getNonAds() {
		return nonAds;
	}

	public void incrementNonAds(int nonAds) {
		this.nonAds = this.nonAds + nonAds;
	}

}
