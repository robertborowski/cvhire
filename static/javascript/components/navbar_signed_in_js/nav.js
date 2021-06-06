class NavbarClass extends HTMLElement {  
  constructor() {
    super();

    // print the variable passed in
    // console.log(this.getAttribute("link_home"));
  }

  connectedCallback() {
    this.innerHTML = `
    <nav class="navbar-signed-in box-shadow-sm-grey box-shadow-rounded">
      <div class="company-name-and-logo">
        <a href="${this.getAttribute("link_home_js")}"><img src="/static/images/logo/Logo.png" class="company-logo" alt="Triviafy icon/logo"></a>
        <h1 class="company-name"><a href="${this.getAttribute("link_home_js")}">Triviafy</a></h1>
      </div>
      <a href="#" class="toggle-button">
        <span class="bar top-bar"></span>
        <span class="bar middle-bar"></span>
        <span class="bar bottom-bar"></span>
      </a>
      <div class="navbar-links">
        <ul>
          <li class="drill-down"><a href="#">Score <i class="fas fa-caret-down"></i></a>
            <ul class="box-shadow-reg-primary box-shadow-rounded sub-list-items">
              <li><a href="${this.getAttribute("link_leaderboard_js")}">Leaderboard</a></li>
              <li><a href="#">Claim Prize</a></li>
            </ul>
          </li>
          <li class="drill-down"><a href="#">Quiz <i class="fas fa-caret-down"></i></a>
            <ul class="box-shadow-reg-primary box-shadow-rounded sub-list-items thicker-ul-item">
              <li><a href="${this.getAttribute("link_quiz_feedback_index_js")}">Feedback</a></li>
              <li><a href="#">Archive</a></li>
              <li><a href="${this.getAttribute("link_create_question_js")}">Create Question</a></li>
              <li><a href="${this.getAttribute("link_quiz_settings_index_js")}">Settings</a></li>
            </ul>
          </li>
          <li class="drill-down"><a href="#">Account <i class="fas fa-caret-down"></i></a>
            <ul class="box-shadow-reg-primary box-shadow-rounded sub-list-items">
              <li><a href="#">Subscription</a></li>
              <li><a href="${this.getAttribute("link_account_js")}">Settings</a></li>
            </ul>
          </li>
        </ul>
      </div>
    </nav>
    <div class="spacer"></div>
    `;
  }
}

customElements.define('nav-component', NavbarClass);