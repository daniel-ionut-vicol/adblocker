package ro.develbox.adblocker;

public class SiteProcessorReport {
	private int pages;
	private int ads;

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

}
