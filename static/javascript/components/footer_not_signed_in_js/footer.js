class FooterNotSignedInClass extends HTMLElement {  
  constructor() {
    super();

    // print the variable passed in
    // console.log(this.getAttribute("link_home"));
  }

  connectedCallback() {
    this.innerHTML = `
    <footer class="footer-not-signed-in">
      <div class="footer-not-signed-in-background">
        <div class="footer-not-signed-in-links">
          <div class="footer-not-signed-in-links-group-1">
            <p class="footer-not-signed-in-links-group-title">Product</p>
            <ul>
              <li><a href="${this.getAttribute("link_home_js")}">Home</a></li>
              <li><a href="${this.getAttribute("link_faq_js")}">FAQ</a></li>
              <li><a href="${this.getAttribute("link_about_js")}">About</a></li>
              <li><a href="${this.getAttribute("pdf_example_quiz_js")}">Example Quiz (PDF)</a></li>
            </ul>
          </div>

          <div class="footer-not-signed-in-links-group-2">
            <p class="footer-not-signed-in-links-group-title">Social</p>
            <ul>
              <li><a href="https://triviafy-app.slack.com/apps/A021726L200-triviafy?tab=more_info" target="_blank">Slack App</a></li>
              <li><a href="https://twitter.com/TriviafyWork" target="_blank">Twitter</a></li>
              <li><a href="https://www.linkedin.com/company/triviafy" target="_blank">LinkedIn</a></li>
              <li><a href="https://medium.com/@robertjborowski/top-3-workplace-trivia-platforms-that-improve-employee-engagement-34953838a86f" target="_blank">Medium</a></li>
            </ul>
          </div>
      
          <div class="footer-not-signed-in-links-group-3">
            <!-- Logo and Company Name -->
            <div class="company-name-and-logo-footer-not-signed-in">
              <!-- Company Name -->
              <p class="footer-not-signed-in-links-group-title">Triviafy</p>
              <!-- Logo -->
              <a href="${this.getAttribute("link_home_js")}"><img src="/static/images/logo/Logo_black_and_white.png" class="company-logo-footer-not-signed-in" alt="Triviafy icon/logo"></a>
            </div>
            <!-- Copyright -->
            <div class="footer-not-signed-in-copyright">
              <p>Copyright © 2021 Triviafy.</p>
              <p>All rights reserved.</p>
              <p class="privacy-and-tos-footer"><a href="${this.getAttribute("link_terms_conditions_js")}">Terms & Conditions</a></p>
              <p class="privacy-and-tos-footer"><a href="${this.getAttribute("link_privacy_js")}">Privacy</a></p>
            </div>
          </div>
        </div>
      </div>
    </footer>
    `;
  }
}

customElements.define('footer-not-signed-in-component', FooterNotSignedInClass);