class FooterNotSignedInClass2 extends HTMLElement {  
  constructor() {
    super();

    // print the variable passed in
    // console.log(this.getAttribute("link_home"));
  }

  connectedCallback() {
    this.innerHTML = `
    <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Footer All - START -->
    <footer class="footer-not-signed-in-2-background-color">
      <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Footer Top - START -->
      <div class="footer-not-signed-in-2-section-top">
        
        <div class="footer-not-signed-in-2-sub-section">
          <p class="footer-title footer-title-position">Product</p>
          <ul class="footer-not-signed-in-2-ul">
            <li class="footer-sub-title-item footer-sub-title-item-position"><a href="${this.getAttribute("pdf_example_quiz_js")}" class="footer-a">Example Quiz</a></li>
            <li class="footer-sub-title-item footer-sub-title-item-position"><a href="${this.getAttribute("pdf_slack_setup_js")}" class="footer-a">Slack Setup</a></li>
          </ul>
        </div>

        <div class="footer-not-signed-in-2-sub-section">
          <p class="footer-title footer-title-position">Resources</p>
          <ul class="footer-not-signed-in-2-ul">
            <li class="footer-sub-title-item footer-sub-title-item-position"><a href="https://slack.com/apps/A021726L200-triviafy?tab=more_info" class="footer-a" target="_blank">Slack App Directory</a></li>
            <li class="footer-sub-title-item footer-sub-title-item-position"><a href="${this.getAttribute("link_faq_js")}" class="footer-a">FAQ</a></li>
            <li class="footer-sub-title-item footer-sub-title-item-position"><a href="${this.getAttribute("link_about_js")}" class="footer-a">About</a></li>
            <li class="footer-sub-title-item footer-sub-title-item-position"><a href="${this.getAttribute("link_blog_js")}" class="footer-a">Blog</a></li>
          </ul>
        </div>

        <div class="footer-not-signed-in-2-sub-section">
          <p class="footer-title footer-title-position">Legal</p>
          <ul class="footer-not-signed-in-2-ul">
            <li class="footer-sub-title-item footer-sub-title-item-position"><a href="${this.getAttribute("link_privacy_js")}" class="footer-a">Privacy</a></li>
            <li class="footer-sub-title-item footer-sub-title-item-position"><a href="${this.getAttribute("link_terms_conditions_js")}" class="footer-a">Terms of Service</a></li>
          </ul>
        </div>
      </div>
      <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Footer Top - END -->

      
      <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Footer Bottom - START -->
      <div class="footer-not-signed-in-2-section-bottom">
        <div class="footer-not-signed-in-2-sub-section-bottom">
          <p class="footer-copyright-2">©2021 Triviafy | All Rights Reserved.</p>
        </div>
        
        <div class="footer-not-signed-in-2-sub-section-bottom">
          <a href="https://twitter.com/TriviafyWork" class="footer-social-logo" target="_blank"><i class="fab fa-twitter-square"></i></a>
          <a href="https://www.linkedin.com/company/triviafy" class="footer-social-logo" target="_blank"><i class="fab fa-linkedin"></i></a>
        </div>
      </div>
      <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Footer Bottom - END -->
    </footer>
    <!-- - - - - - - - - - - - - - - - - - - - - - - - - - - Footer All - END -->
    `;
  }
}

customElements.define('footer-not-signed-in-component-2', FooterNotSignedInClass2);