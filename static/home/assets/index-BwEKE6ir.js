var js=Object.defineProperty;var Hs=(s,e,t)=>e in s?js(s,e,{enumerable:!0,configurable:!0,writable:!0,value:t}):s[e]=t;var y=(s,e,t)=>Hs(s,typeof e!="symbol"?e+"":e,t);(function(){const e=document.createElement("link").relList;if(e&&e.supports&&e.supports("modulepreload"))return;for(const n of document.querySelectorAll('link[rel="modulepreload"]'))a(n);new MutationObserver(n=>{for(const i of n)if(i.type==="childList")for(const c of i.addedNodes)c.tagName==="LINK"&&c.rel==="modulepreload"&&a(c)}).observe(document,{childList:!0,subtree:!0});function t(n){const i={};return n.integrity&&(i.integrity=n.integrity),n.referrerPolicy&&(i.referrerPolicy=n.referrerPolicy),n.crossOrigin==="use-credentials"?i.credentials="include":n.crossOrigin==="anonymous"?i.credentials="omit":i.credentials="same-origin",i}function a(n){if(n.ep)return;n.ep=!0;const i=t(n);fetch(n.href,i)}})();function Vt(){return`
    <div class="min-h-screen bg-gradient-to-br from-base-200 to-base-300">
      <!-- Responsive Sticky Navbar -->
      <div class="navbar bg-base-100/90 backdrop-blur-md rounded-box ml-0 mr-2 sm:mx-4 lg:mx-auto mt-2 max-w-6xl shadow-lg fixed top-0 left-0 right-0 z-50">
          <!-- Logo/Brand - Left side -->
          <div class="navbar-start">
              <a class="text-xl sm:text-2xl lg:text-3xl font-semibold poppins gradient-text tracking-tight">
                  &nbsp;Vibe<span class="font-bold">Reach</span>
              </a>
          </div>
          
          <!-- Desktop menu - Center -->
          <div class="navbar-center hidden lg:flex">
              <ul class="menu menu-horizontal gap-2 px-1">
                  <li><a href="#how-it-works" class="text-lg font-medium hover:bg-base-200 rounded-btn transition-colors">How it works</a></li>
                  <li><a href="#features" class="text-lg font-medium hover:bg-base-200 rounded-btn transition-colors">Features</a></li>
                  <li><a class="text-lg font-medium hover:bg-base-200 rounded-btn transition-colors">All About the Beta</a></li>
              </ul>
          </div>
          
          <!-- Right side - CTA Button + Mobile Menu -->
          <div class="navbar-end">
              <!-- CTA Button - hidden on very small screens, visible on sm and up -->
              <a href="#early-access" class="btn btn-primary text-lg px-6 hidden md:inline-flex">Get Early Access</a>
          
              <!-- Mobile hamburger menu -->
              <div class="dropdown dropdown-end lg:hidden">
                  <div tabindex="0" role="button" class="btn btn-ghost btn-circle">
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h8m-8 6h16" />
                      </svg>
                  </div>
                  <!-- Mobile menu dropdown -->
                  <ul tabindex="0" class="menu menu-sm dropdown-content bg-base-100 rounded-box z-[1] mt-3 w-52 p-2 shadow-xl border border-base-300">
                      <li><a href="#how-it-works" class="text-base font-medium py-3">How it works</a></li>
                      <li><a href="#features" class="text-base font-medium py-3">Features</a></li>
                      <li><a class="text-base font-medium py-3">All About the Beta</a></li>
                      <li class="mt-2 pt-2 border-t border-base-300">
                          <a href="#early-access" class="btn btn-primary btn-sm w-full">Get Early Access</a>
                      </li>
                  </ul>
              </div>
          </div>
      </div>
    

      <!-- Hero Section -->
      <div class="container mx-auto px-6 py-16">
          <div class="hero min-h-[85vh]">
              <!-- Only change flex direction on small screens -->
              <div class="hero-content flex-col lg:flex-row-reverse gap-16 max-w-7xl pt-14 lg:pt-0">
                  <!-- Hero Image/Visual - now comes first in DOM for mobile -->
                  <div class="flex-1 flex justify-center order-1 lg:order-none">
                      <img src="/static/home/hero.webp" class="w-full max-w-md lg:max-w-none">
                  </div>

                  <!-- Hero Text -->
                  <div class="flex-1 text-center lg:text-left">
                      <div class="badge badge-primary badge-outline text-base p-3 mb-4 hidden md:inline-flex">
                          🚀 B2B OUTREACH REVOLUTION
                      </div>
                      <h1 class="text-5xl lg:text-7xl font-bold gradient-text mb-6 leading-tight">
                          Turn Cold Emails Into 
                          <span class="text-primary">Hot Leads</span>
                      </h1>
                      <p class="text-xl text-base-content/80 mb-8 leading-relaxed max-w-2xl mx-auto lg:mx-0">
                          Engage potential leads through personalized, AI-powered cold outreach across email. Capture attention with relevant messaging tailored to each prospect's industry and needs.
                      </p>

                      <!-- Key Benefits -->
                      <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
                          <div class="flex items-center gap-3 hidden md:inline-flex">
                              <div class="w-10 h-10 bg-primary/10 rounded-full flex items-center justify-center">
                                  <i class="fas fa-brain text-primary"></i>
                              </div>
                              <span class="font-medium">AI-Powered Personalization</span>
                          </div>
                          <div class="flex items-center gap-3 justify-center lg:justify-start">
                              <div class="w-10 h-10 bg-secondary/10 rounded-full flex items-center justify-center">
                                  <i class="fas fa-chart-line text-secondary"></i>
                              </div>
                              <span class="font-medium">3x Higher Response Rates</span>
                          </div>
                          <div class="flex items-center gap-3 justify-center lg:justify-start">
                              <div class="w-10 h-10 bg-accent/10 rounded-full flex items-center justify-center">
                                  <i class="fas fa-clock text-accent"></i>
                              </div>
                              <span class="font-medium">Save 10+ Hours Weekly</span>
                          </div>
                          <div class="flex items-center gap-3 hidden md:inline-flex">
                              <div class="w-10 h-10 bg-info/10 rounded-full flex items-center justify-center">
                                  <i class="fas fa-bullseye text-info"></i>
                              </div>
                              <span class="font-medium">Precision Targeting</span>
                          </div>
                      </div>

                      <div class="flex flex-col sm:flex-row gap-4 justify-center lg:justify-start">
                          <a href="#early-access" class="btn btn-primary btn-lg gap-2 hover:scale-105 transition-transform shadow-lg">
                              <i class="fas fa-rocket"></i>
                              Join Waitlist
                          </a>
                          <a href="https://gataraai.zohobookings.com/#/ceo-call" class="btn btn-outline btn-lg gap-2 hidden md:inline-flex">
                              <i class="fas fa-play"></i>
                              Book Demoo
                          </a>
                      </div>

                      <br>

                      <div class="space-y-4 flex justify-center lg:justify-start">
                          <a href="#hormozi-style-headline-generator" class="btn btn-primary text-lg py-4 px-6 h-auto min-h-[3.5rem] sm:min-h-0 gap-2 hover:scale-105 transition-transform third-hero-btn">
                              <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                              </svg>
                              Generate Hormozi-Style Headlines
                          </a>
                      </div>
                  </div>
              </div>
          </div>
      </div>

      
      <!-- How It Works Section -->
      <div id="how-it-works" class="bg-base-100 px-0 sm:px-6 py-20">
          <div class="container mx-auto px-0 sm:px-6">
              <div class="text-center mb-16 px-5 sm:px-0">
                  <div class="badge badge-primary badge-outline text-lg p-3 mb-4">
                      HOW IT WORKS
                  </div>
                  <h2 class="text-4xl lg:text-5xl font-bold mb-6">From Lead List to Closed Deals</h2>
                  <p class="text-xl text-base-content/70 max-w-3xl mx-auto">
                      Our AI-powered platform transforms your cold outreach process in three simple steps
                  </p>
              </div>

              <!-- Process Flow -->
            <div class="max-w-6xl mx-auto mb-[10vh] px-5 sm:px-0">
            <div class="relative grid grid-cols-1 lg:grid-cols-3 gap-8">
                <!-- Step 1 -->
                <div class="flex flex-col h-full">
                    <div class="card bg-gradient-to-br from-primary/5 to-primary/10 border border-primary/20 shadow-xl hover:shadow-2xl transition-all duration-300 h-full">
                        <div class="card-body text-center p-8 flex flex-col justify-between">
                            <div>
                                <div class="w-16 h-16 bg-primary rounded-full flex items-center justify-center mx-auto mb-6">
                                    <i class="fas fa-upload text-2xl text-primary-content"></i>
                                </div>
                                <h3 class="text-2xl font-bold mb-6">1. Upload Your Leads</h3>
                            </div>
                            <div>
                              <p class="text-base-content/70 mb-6">
                                  Import your lead list with their info, LinkedIn profiles, and company websites. Our AI does the rest.
                              </p>
                            </div>
                            <div class="mockup-code bg-base-200 text-left !pt-0">
                                <div class="overflow-x-auto text-primary -mt-4">
                                    <table class="table table-xs">
                                        <thead>
                                            <tr>
                                                <th></th>
                                                <th>Name</th>
                                                <th>Headline</th>
                                                <th>About</th>
                                                <th>Position</th>
                                                <th>Company</th>
                                                <th>Company About</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr>
                                                <th>1</th>
                                                <td>Sarah Johnson</td>
                                                <td>Sarah's Headline</td>
                                                <td>Sarah's About</td>
                                                <td>Sarah's Position</td>
                                                <td>Sarah's Company</td>
                                                <td>Company About</td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>  
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Arrow 1 - Positioned between cards -->
                <div class="hidden lg:block absolute left-1/3 top-1/2 transform -translate-x-1/2 -translate-y-1/2 text-primary text-2xl z-10">
                    <i class="fas fa-arrow-right"></i>
                </div>

                <!-- Step 2 -->
                <div class="flex flex-col h-full">
                    <div class="card bg-gradient-to-br from-secondary/5 to-secondary/10 border border-secondary/20 shadow-xl hover:shadow-2xl transition-all duration-300 h-full">
                        <div class="card-body text-center p-8 flex flex-col justify-between">
                            <div>
                                <div class="w-16 h-16 bg-secondary rounded-full flex items-center justify-center mx-auto mb-6">
                                    <i class="fas fa-robot text-2xl text-secondary-content"></i>
                                </div>
                                <h3 class="text-2xl font-bold mb-6">2. AI Analyzes & Personalizes</h3>
                            </div>
                            <div
                              <p class="text-base-content/70 mb-6">
                                    Our AI Get the lead's data, creates personalized messages using your own business tone and style.
                              </p>
                            </div>
                            <div class="bg-base-200 rounded-lg p-4 text-left">
                                <div class="flex items-center gap-2 mb-2">
                                    <div class="loading loading-spinner loading-2xs text-secondary" style="width: 1.2rem; height: 1.2rem;"></div>
                                    <span class="text-sm">Analyzing Prospect's Data...</span>
                                </div>
                                <div class="flex items-center gap-2 mb-2">
                                    <i class="fas fa-check text-success text-sm"></i>
                                    <span class="text-sm">Applying your Business Tone and Style</span>
                                </div>
                                <div class="flex items-center gap-2">
                                    <i class="fas fa-check text-success text-sm"></i>
                                    <span class="text-sm">Personalized message ready</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Arrow 2 - Positioned between cards -->
                <div class="hidden lg:block absolute left-2/3 top-1/2 transform -translate-x-1/2 -translate-y-1/2 text-secondary text-2xl z-10">
                    <i class="fas fa-arrow-right"></i>
                </div>

                <!-- Step 3 -->
                <div class="flex flex-col h-full">
                    <div class="card bg-gradient-to-br from-accent/5 to-accent/10 border border-accent/20 shadow-xl hover:shadow-2xl transition-all duration-300 h-full">
                        <div class="card-body text-center p-8 flex flex-col justify-between">
                            <div>
                                <div class="w-16 h-16 bg-accent rounded-full flex items-center justify-center mx-auto mb-4">
                                    <i class="fas fa-paper-plane text-2xl text-accent-content"></i>
                                </div>
                                <h3 class="text-2xl font-bold mb-4">3. Send & Track Results</h3>
                            </div>
                            <div>
                               <p class="text-base-content/70 mb-6">
                                  Send personalized emails and track every interaction with detailed analytics.
                               </p>
                            </div>
                            <div class="stats stats-vertical shadow bg-base-100">
                                <div class="stat py-3">
                                    <div class="stat-title text-xs">Delivered</div>
                                    <div class="stat-value text-success text-lg">98%</div>
                                </div>
                                <div class="stat py-3">
                                    <div class="stat-title text-xs">Opened</div>
                                    <div class="stat-value text-primary text-lg">72%</div>
                                </div>
                                <div class="stat py-3">
                                    <div class="stat-title text-xs">Replied</div>
                                    <div class="stat-value text-accent text-lg">34%</div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    


      <!-- =============================================== -->
      <!-- START: NEW AI PERSONALIZATION FEATURES SECTION -->
      <!-- =============================================== -->
      <div class="container mx-auto px-0 sm:px-6 py-20">
        <div class="hero">
          <div class="hero-content flex-col lg:flex-row items-center gap-12 lg:gap-20">

            <!-- Visual Side: Tone & Style Comparison -->
            <div class="flex-1 w-full lg:order-last order-1">
              <div class="bg-base-200/60 p-4 sm:p-6 rounded-2xl shadow-lg">
                <div class="flex flex-col items-center gap-4">

                  <!-- Step 1: User provides their style -->
                  <div class="w-full">
                    <p class="text-sm font-semibold text-base-content/60 mb-2 text-center">Generic Template</p>
                    <div class="mockup-window border bg-neutral">
                      <div class="p-4 bg-neutral-focus text-neutral-content font-mono text-xs leading-relaxed">
                        <p class="whitespace-pre-wrap">Hi {first_name},</p>
                        <p class="whitespace-pre-wrap mt-2 text-warning">I saw your company {company_name}...</p>
                        <p class="whitespace-pre-wrap mt-2 text-warning">I think we can help.</p>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Processing Icon -->
                  <div class="flex flex-col items-center my-2">
                      <i class="fas fa-robot text-4xl text-primary mb-2"></i>
                      <i class="fas fa-arrow-down text-2xl text-base-content/40 mt-2"></i>
                  </div>

                  <!-- Step 2: AI generates in that style -->
                  <div class="w-full">
                    <p class="text-sm font-semibold text-secondary mb-2 text-center">AI-Personalized & Stylized</p>
                    <div class="mockup-window border bg-neutral">
                      <div class="p-4 bg-neutral-focus text-neutral-content font-mono text-xs leading-relaxed">
                        <p class="whitespace-pre-wrap">Hi Alex,</p>
                        <p class="whitespace-pre-wrap mt-2 text-success">Curious — how are you currently handling cold outreach <span class="badge badge-secondary font-bold">MediaAI</span>?</p>
                        <p class="whitespace-pre-wrap mt-2 text-success">What would it look like if every prospect you emailed felt like the message was written <span class="badge badge-secondary font-bold">just</span> for them?</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>


            <!-- Text Side: Features & Benefits -->
            <div class="flex-1 text-center lg:text-left px-1 order-0">
              <div class="badge badge-primary badge-outline text-lg p-3 mb-4 font-semibold">
                PERSONALIZATION
              </div>
              <h2 class="text-4xl lg:text-5xl font-bold mb-4">Go Beyond <code class="text-primary">{first_name}</code></h2>
              <p class="text-lg text-base-content/80 mb-6 leading-relaxed">
                Our AI analyzes your lead's information and your company's unique voice to craft emails that are personlized to get you the result.
              </p>
              <ul class="space-y-4">
                <li class="flex items-start justify-center lg:justify-start gap-3">
                  <i class="fas fa-check-circle text-secondary mt-1.5"></i>
                  <span>Analyzes lead's data, experince, and their company for relevant insights.</span>
                </li>
                <li class="flex items-start justify-center lg:justify-start gap-3">
                  <i class="fas fa-check-circle text-secondary mt-1.5"></i>
                  <span>Adapts to your business tone and style for branded communication.</span>
                </li>
                <li class="flex items-start justify-center lg:justify-start gap-3">
                  <i class="fas fa-check-circle text-secondary mt-1.5"></i>
                  <span>Generates personlized opening lines that build trust.</span>
                </li>
              </ul>
            </div>

          </div>
        </div>
      </div>
      <!-- =============================================== -->
      <!-- END: NEW AI PERSONALIZATION FEATURES SECTION   -->
      <!-- =============================================== -->





      <!-- =============================================== -->
      <!-- START: NEW LINK TRACKING FEATURES SECTION (Corrected Contrast) -->
      <!-- =============================================== -->
      <div class="container mx-auto px-0 sm:px-6 py-20 bg-base-200">
        <div class="hero">
          <div class="hero-content flex-col lg:flex-row items-center gap-12 lg:gap-20">

            <!-- Visual Side: Link Tracking Process -->
            <div class="flex-1 w-full order-1 lg:order-last">
              <div class="bg-base-200/60 p-4 sm:p-6 rounded-2xl shadow-lg">
                <div class="flex flex-col items-center gap-4">

                  <!-- Step 1: Email with a standard link -->
                  <div class="w-full">
                    <p class="text-sm font-semibold text-base-content/60 mb-2 text-center">Your Original Email</p>
                    <!-- Email Window -->
                    <div class="bg-neutral rounded-lg shadow-md">
                      <div class="flex items-center gap-2 p-3 bg-neutral-focus/30 rounded-t-lg">
                        <div class="w-3 h-3 rounded-full bg-base-content/20"></div>
                        <div class="w-3 h-3 rounded-full bg-base-content/20"></div>
                        <div class="w-3 h-3 rounded-full bg-base-content/20"></div>
                      </div>
                      <div class="p-4 font-mono text-sm leading-relaxed text-neutral-content">
                        <p>...P.S. Here’s a quick look at the product I mentioned:</p>
                        <a href="#" class="link link-primary">outreach.gatara.org</a>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Processing Icon -->
                  <div class="flex flex-col items-center my-2">
                      <i class="fas fa-chart-line text-4xl text-primary"></i>
                      <i class="fas fa-arrow-down text-2xl text-base-content/40 mt-2"></i>
                  </div>

                  <!-- Step 2: The Analytics Result -->
                  <div class="w-full">
                    <p class="text-sm font-semibold text-secondary mb-2 text-center">Actionable Engagement Report</p>
                    <div class="card bg-neutral text-neutral-content shadow-md">
                      <div class="card-body p-5">
                        <h4 class="card-title text-base text-neutral-content">Report for: Alex Johnson - Email #3/Campaign #1</h4>
                        
                        <!-- CORRECTED STATS COMPONENT -->
                        <div class="stats stats-vertical sm:stats-horizontal shadow bg-base-100 my-2">
                          <div class="stat p-3">
                            <div class="stat-title">Total Clicks</div>
                            <div class="stat-value text-base-content text-2xl">2</div>
                          </div>
                          <div class="stat p-3">
                            <div class="stat-title">Lead Status</div>
                            <div class="stat-value text-error text-2xl">Interested</div>
                          </div>
                        </div>
                        
                        <div class="mt-2">
                          <!-- CORRECTED TEXT COLOR -->
                          <p class="text-sm font-semibold text-neutral-content mb-0">Click Details:</p>
                          <p class="text-sm  text-neutral-content mb-2">{this can be discovered via UTM sources on your website}</p>
                          <ul class="text-xs font-mono space-y-1 text-neutral-content">
                            <li>- <span class="font-bold">/case-study</span> (4 times)</li>
                            <li>- <span class="font-bold">/pricing</span> (2 times)</li>
                            <li>- <span class="font-bold">/about-us</span> (1 time)</li>
                          </ul>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Text Side: Features & Benefits (Unchanged) -->
            <div class="flex-1 text-center lg:text-left px-1 order-0">
              <div class="badge badge-primary badge-outline text-lg p-3 mb-4 font-semibold">
                PRECISION ANALYTICS
              </div>
              <h2 class="text-4xl lg:text-5xl font-bold mb-4">Track Every Click, Uncover Intent</h2>
              <p class="text-lg text-base-content/80 mb-6 leading-relaxed">
                Stop guessing. Our system automatically converts every link into a unique, trackable URL for each prospect. See exactly who is engaging <span class="text-primary">{by VibeReach}</span> and what they're interested in to prioritize your follow-ups <span class="text-accent">{by tracking UTM sources on your website}</span>.
              </p>
              <ul class="space-y-4">
                <li class="flex items-start justify-center lg:justify-start gap-3">
                  <i class="fas fa-check-circle text-secondary mt-1.5"></i>
                  <span>Unique tracking links are generated for each prospect and each email.</span>
                </li>
                <li class="flex items-start justify-center lg:justify-start gap-3">
                  <i class="fas fa-check-circle text-secondary mt-1.5"></i>
                  <span>Identify which links get clicked to understand what content resonates most.</span>
                </li>
                <li class="flex items-start justify-center lg:justify-start gap-3">
                  <i class="fas fa-check-circle text-secondary mt-1.5"></i>
                  <span>Get insights to identify "interested leads" who are actively exploring your solution.</span>
                </li>
              </ul>
            </div>

          </div>
        </div>
      </div>
      <!-- =============================================== -->
      <!-- END: NEW LINK TRACKING FEATURES SECTION        -->
      <!-- =============================================== -->


      <!-- =============================================== -->
      <!-- START: NEW AUTHENTIC TONE FEATURES SECTION      -->
      <!-- =============================================== -->
      <div class="container mx-auto px-0 sm:px-6 py-20">
        <div class="hero">
          <div class="hero-content flex-col lg:flex-row items-center gap-12 lg:gap-20">

            <!-- Visual Side: Tone & Style Comparison -->
            <div class="flex-1 w-full lg:order-last order-1">
              <div class="bg-base-200/60 p-4 sm:p-6 rounded-2xl shadow-lg">
                <div class="flex flex-col items-center gap-4">

                  <!-- Step 1: User provides their style -->
                  <div class="w-full">
                    <p class="text-sm font-semibold text-base-content/60 mb-2 text-center">1. Provide Your Style Examples</p>
                    <div class="mockup-window border bg-neutral">
                      <div class="p-4 bg-neutral-focus text-neutral-content font-mono text-xs leading-relaxed">
                        <p class="whitespace-pre-wrap">Hey {{first_name}}, how do you do cold outreach at {{company_name}}?</p>
                        <p class="whitespace-pre-wrap mt-2">A lot of SaaS teams either send the same templated stuff that gets ignored, or they have something great to offer but it gets buried.</p>
                        <p class="whitespace-pre-wrap mt-2">What if every email felt like it was written just for that one lead?</p>
                        <p class="whitespace-pre-wrap mt-2">...</p>
                      </div>
                    </div>
                  </div>
                  
                  <!-- Processing Icon -->
                  <div class="flex flex-col items-center my-2">
                      <i class="fas fa-palette text-4xl text-primary"></i>
                      <i class="fas fa-arrow-down text-2xl text-base-content/40 mt-2"></i>
                  </div>

                  <!-- Step 2: AI generates in that style -->
                  <div class="w-full">
                    <p class="text-sm font-semibold text-secondary mb-2 text-center">2. AI Generates In Your Voice</p>
                    <div class="mockup-window border bg-neutral">
                      <div class="p-4 bg-neutral-focus text-neutral-content font-mono text-xs leading-relaxed">
                        <p class="whitespace-pre-wrap">Hi {{FirstName}},</p>
                        <p class="whitespace-pre-wrap mt-2">Curious — how are you currently handling cold outreach at {{CompanyName}}?</p>
                        <p class="whitespace-pre-wrap mt-2">Most software teams I speak with either:</p>
                        <ol>
                          <li class="whitespace-pre-wrap mt-2">1. Send the same templated stuff that gets ignored</li>
                          <li class="whitespace-pre-wrap mt-2">2. Have something great to offer but it gets buried</li>
                        </ol>
                        <p class="whitespace-pre-wrap mt-2">What would it look like if every prospect you emailed felt like the message was written *just* for them?</p>
                        <p class="whitespace-pre-wrap mt-2">...</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Text Side: Features & Benefits -->
            <div class="flex-1 text-center lg:text-left px-1 order-0">
              <div class="badge badge-primary badge-outline text-lg p-3 mb-4 font-semibold">
                AUTHENTIC MESSAGING
              </div>
              <h2 class="text-4xl lg:text-5xl font-bold mb-4">Your Voice,<br>Amplified by AI</h2>
              <p class="text-lg text-base-content/80 mb-6 leading-relaxed">
                Generic outreach doesn't work. Feed our AI examples of your writing—your own buisness tone and style—and it communicate with your unique tone, vocabulary, and style. The result is outreach that is authentically *yours*.
              </p>
              <ul class="space-y-4">
                <li class="flex items-start justify-center lg:justify-start gap-3">
                  <i class="fas fa-check-circle text-secondary mt-1.5"></i>
                  <span>Maintains your brand consistency across all outreach.</span>
                </li>
                <li class="flex items-start justify-center lg:justify-start gap-3">
                  <i class="fas fa-check-circle text-secondary mt-1.5"></i>
                  <span>Builds genuine transperancy & trust by sounding like a human, not a generic template, or AI ;)</span>
                </li>
                <li class="flex items-start justify-center lg:justify-start gap-3">
                  <i class="fas fa-check-circle text-secondary mt-1.5"></i>
                  <span>Eliminates the need to constantly edit and rewrite AI-generated text.</span>
                </li>
              </ul>
            </div>

          </div>
        </div>
      </div>
      <!-- =============================================== -->
      <!-- END: NEW AUTHENTIC TONE FEATURES SECTION       -->
      <!-- =============================================== -->


        <!-- =============================================== -->
        <!-- START: NEW ROI ANALYTICS FEATURES SECTION (Corrected for Readability) -->
        <!-- =============================================== -->
        <div class="container mx-auto px-0 sm:px-6 py-20 bg-base-200">
          <div class="hero">
            <div class="hero-content flex-col lg:flex-row items-center gap-12 lg:gap-20">

              <!-- Visual Side: The ROI Dashboard -->
              <div class="flex-1 w-full order-1 lg:order-last">
                <div class="bg-base-200/60 p-4 sm:p-6 rounded-2xl shadow-lg">
                  <div class="card bg-neutral text-neutral-content shadow-xl">
                    <div class="card-body p-6">
                      <h3 class="card-title text-neutral-content mb-4">Campaign Performance: Q3</h3>
                      
                      <!-- Key Metrics with a LIGHT background for contrast -->
                      <div class="stats stats-vertical sm:stats-horizontal shadow bg-base-100 text-base-content rounded-lg">
                        <div class="stat p-4">
                          <div class="stat-figure text-secondary">
                            <i class="fas fa-user-plus text-3xl"></i>
                          </div>
                          <div class="stat-title">New Customers</div>
                          <div class="stat-value text-base-content">32</div>
                          <div class="stat-desc">22% increase</div>
                        </div>
                        
                        <div class="stat p-4">
                          <div class="stat-figure text-success">
                            <i class="fas fa-dollar-sign text-3xl"></i>
                          </div>
                          <div class="stat-title">New Revenue</div>
                          <div class="stat-value text-success">$41,800</div>
                          <div class="stat-desc">From this campaign</div>
                        </div>
                      </div>

                      <!-- Chart Area -->
                      <div class="mt-6">
                        <!-- CORRECTED: Text is now bright and readable -->
                        <p class="font-bold text-neutral-content mb-2">Lead Engagement & Conversion</p>
                        
                        <!-- Mock SVG Chart on the dark card background -->
                        <div class="w-full rounded-lg">
                            <svg class="w-full h-32" viewBox="0 0 200 100" preserveAspectRatio="none">
                                <!-- Grid Lines -->
                                <line x1="0" y1="25" x2="200" y2="25" stroke-width="0.5" class="stroke-current text-neutral-content/20"/>
                                <line x1="0" y1="50" x2="200" y2="50" stroke-width="0.5" class="stroke-current text-neutral-content/20"/>
                                <line x1="0" y1="75" x2="200" y2="75" stroke-width="0.5" class="stroke-current text-neutral-content/20"/>
                                <!-- Data Lines -->
                                <path d="M 0 80 L 40 70 L 80 50 L 120 55 L 160 30 L 200 20" fill="none" stroke-width="2.5" class="stroke-current text-secondary"/>
                                <path d="M 0 90 L 40 85 L 80 75 L 120 65 L 160 55 L 200 50" fill="none" stroke-width="2.5" class="stroke-current text-primary"/>
                            </svg>
                        </div>
                        <!-- CORRECTED: Legend text is now bright and readable -->
                        <div class="flex justify-center gap-6 mt-2 text-xs text-neutral-content">
                              <div class="flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-secondary"></span>Engagement</div>
                              <div class="flex items-center gap-2"><span class="w-3 h-3 rounded-full bg-primary"></span>Conversions</div>
                          </div>
                      </div>

                    </div>
                  </div>
                </div>
              </div>

              <!-- Text Side: Features & Benefits (Unchanged) -->
              <div class="flex-1 text-center lg:text-left px-1 order-0">
                <div class="badge badge-primary badge-outline text-lg p-3 mb-4 font-semibold">
                  MEASURABLE RESULTS
                </div>
                <h2 class="text-4xl lg:text-5xl font-bold mb-4">Connect Outreach to Revenue</h2>
                <p class="text-lg text-base-content/80 mb-6 leading-relaxed">
                  Don't just measure opens and clicks. Our comprehensive dashboard connects your outreach efforts directly to bottom-line results, so you can see the true ROI of every campaign and make intelligent, data-driven decisions.
                </p>
                <ul class="space-y-4">
                  <li class="flex items-start justify-center lg:justify-start gap-3">
                    <i class="fas fa-check-circle text-secondary mt-1.5"></i>
                    <span>Attribute new customers and revenue directly to specific outreach campaigns.</span>
                  </li>
                  <li class="flex items-start justify-center lg:justify-start gap-3">
                    <i class="fas fa-check-circle text-secondary mt-1.5"></i>
                    <span>Visualize engagement trends to understand what drives conversions over time.</span>
                  </li>
                  <li class="flex items-start justify-center lg:justify-start gap-3">
                    <i class="fas fa-check-circle text-secondary mt-1.5"></i>
                    <span>Confidently report on performance and justify your marketing spend with hard data.</span>
                  </li>
                </ul>
              </div>

            </div>
          </div>
        </div>
        <!-- =============================================== -->
        <!-- END: NEW ROI ANALYTICS FEATURES SECTION        -->
        <!-- =============================================== -->



        <!-- Email Comparison Section -->
        <div class="container mx-auto px-6 py-20">
            <div class="text-center mb-16">
                <div class="badge badge-primary badge-outline text-lg p-3 mb-4">
                    BEFORE VS AFTER
                </div>
                <h2 class="text-4xl lg:text-5xl font-bold mb-6">See the Difference AI Makes</h2>
                <p class="text-xl text-base-content/70 max-w-3xl mx-auto">
                    Compare generic templates with our AI-powered personalized emails
                </p>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-6xl mx-auto">
                <!-- Generic Email -->
                <div class="space-y-4">
                    <div class="flex items-center gap-3 mb-4">
                        <div class="w-10 h-10 bg-error/10 rounded-full flex items-center justify-center">
                            <i class="fas fa-times text-error"></i>
                        </div>
                        <h3 class="text-2xl font-bold text-error">Generic Template</h3>
                    </div>
                    
                    <div class="mockup-browser border border-error/20 bg-base-100">
                        <div class="mockup-browser-toolbar">
                            <div class="input border border-base-300">Email Client</div>
                        </div>
                        <div class="p-6 border-t border-base-300 email-mockup">
                            <div class="border-b border-base-300 pb-4 mb-4">
                                <div class="flex items-center gap-3 mb-2">
                                    <div class="w-8 h-8 bg-base-300 rounded-full"></div>
                                    <div>
                                        <div class="font-semibold">sales@yourcompany.com</div>
                                        <div class="text-sm text-base-content/60">to: prospect@company.com</div>
                                    </div>
                                </div>
                                <div class="text-lg font-semibold">Partnership Opportunity</div>
                            </div>
                            
                            <div class="space-y-3 text-sm">
                                <p>Hi [First Name],</p>
                                <p>I hope this email finds you well. I wanted to reach out regarding a potential partnership opportunity with [Company Name].</p>
                                <p>Our company specializes in helping businesses like yours increase their revenue. I think we can help you too.</p>
                                <p>Would you be interested in a quick 15-minute call to discuss this further?</p>
                                <p>Best regards,<br>John Smith</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="alert alert-error">
                        <i class="fas fa-exclamation-triangle"></i>
                        <span><strong>Problems:</strong> Generic, impersonal, no research, low response rate</span>
                    </div>
                </div>

                <!-- AI-Powered Email -->
                <div class="space-y-4">
                    <div class="flex items-center gap-3 mb-4">
                        <div class="w-10 h-10 bg-success/10 rounded-full flex items-center justify-center">
                            <i class="fas fa-check text-success"></i>
                        </div>
                        <h3 class="text-2xl font-bold text-success">AI-Powered Email</h3>
                    </div>
                    
                    <div class="mockup-browser border border-success/20 bg-base-100">
                        <div class="mockup-browser-toolbar">
                            <div class="input border border-base-300">Email Client</div>
                        </div>
                        <div class="p-6 border-t border-base-300 email-mockup">
                            <div class="border-b border-base-300 pb-4 mb-4">
                                <div class="flex items-center gap-3 mb-2">
                                    <div class="w-8 h-8 bg-primary rounded-full flex items-center justify-center text-white text-xs">AH</div>
                                    <div>
                                        <div class="font-semibold">ahmad@vibereach.com</div>
                                        <div class="text-sm text-base-content/60">to: sarah@techstart.com</div>
                                    </div>
                                </div>
                                <div class="text-lg font-semibold">Congrats on the TechStart Series A! 🚀</div>
                            </div>
                            
                            <div class="space-y-3 text-sm">
                                <p>Hi Sarah,</p>
                                <p>Just saw the news about TechStart's $5M Series A on TechCrunch - huge congratulations! The AI-powered customer service platform sounds like it's solving a real pain point.</p>
                                <p>I noticed from your LinkedIn post that you're scaling the sales team rapidly. At VibeReach, we've helped companies like yours increase their outbound response rates by 300% during growth phases.</p>
                                <p>Given TechStart's focus on AI, I thought you might find our approach interesting - we use AI to personalize cold outreach at scale, which might be perfect as you're building your enterprise sales motion.</p>
                                <p>Would you be open to a brief conversation about how we've helped similar AI startups accelerate their sales pipeline?</p>
                                <p>Best,<br>Ahmad</p>
                                <p class="text-xs text-base-content/60">P.S. - Love the company's mission of "making customer service human again"</p>
                            </div>
                        </div>
                    </div>
                    
                    <div class="alert alert-success">
                        <i class="fas fa-check-circle"></i>
                        <span><strong>Results:</strong> Personal, researched, relevant, 3x higher response rate</span>
                    </div>
                </div>
            </div>
        </div>




    <!-- Features Section -->
    <div id="features" class="bg-base-200/60 py-20">
        <div class="container mx-auto px-6">
            <div class="text-center mb-16">
                <div class="badge badge-primary badge-outline text-lg p-3 mb-4">
                    FEATURES
                </div>
                <h2 class="text-4xl lg:text-5xl font-bold mb-6">Everything You Need to Scale Outreach</h2>
                <p class="text-xl text-base-content/70 max-w-3xl mx-auto">
                    Powerful features designed to maximize your outreach ROI
                </p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-7xl mx-auto">
                <!-- Feature 1 -->
                <div class="card bg-base-100 shadow-xl border border-base-300 hover:shadow-2xl transition-all duration-300">
                    <div class="card-body p-8">
                        <div class="w-16 h-16 bg-primary/10 rounded-xl flex items-center justify-center mb-4">
                            <i class="fas fa-brain text-primary text-3xl"></i>
                        </div>
                        <h3 class="text-xl font-bold mb-3">AI Research Assistant</h3>
                        <p class="text-base-content/70">
                            Automatically analyzes LinkedIn profiles, company websites, and recent news to find personalization opportunities.
                        </p>
                    </div>
                </div>

                <!-- Feature 2 -->
                <div class="card bg-base-100 shadow-xl border border-base-300 hover:shadow-2xl transition-all duration-300">
                    <div class="card-body p-8">
                        <div class="w-16 h-16 bg-secondary/10 rounded-xl flex items-center justify-center mb-4">
                            <i class="fas fa-palette text-secondary text-3xl"></i>
                        </div>
                        <h3 class="text-xl font-bold mb-3">Voice & Tone Matching</h3>
                        <p class="text-base-content/70">
                            Your buisness tone and style, the result outreach that is authentically *yours*.
                        </p>
                    </div>
                </div>

                <!-- Feature 3 -->
                <div class="card bg-base-100 shadow-xl border border-base-300 hover:shadow-2xl transition-all duration-300">
                    <div class="card-body p-8">
                        <div class="w-16 h-16 bg-accent/10 rounded-xl flex items-center justify-center mb-4">
                            <i class="fas fa-chart-line text-accent text-3xl"></i>
                        </div>
                        <h3 class="text-xl font-bold mb-3">Advanced Analytics</h3>
                        <p class="text-base-content/70">
                            Track opens, clicks, replies, and conversions with relevant insights to operate based on math, not guess work.
                        </p>
                    </div>
                </div>

                <!-- Feature 4 -->
                <div class="card bg-base-100 shadow-xl border border-base-300 hover:shadow-2xl transition-all duration-300">
                    <div class="card-body p-8">
                        <div class="w-16 h-16 bg-info/10 rounded-xl flex items-center justify-center mb-4">
                            <i class="fas fa-sync text-info text-3xl"></i>
                        </div>
                        <h3 class="text-xl font-bold mb-3">Email Sequence</h3>
                        <p class="text-base-content/70">
                            Schedules emails based on the Campaign email sequence you make.
                        </p>
                    </div>
                </div>

                <!-- Feature 5 -->
                <div class="card bg-base-100 shadow-xl border border-base-300 hover:shadow-2xl transition-all duration-300">
                    <div class="card-body p-8">
                        <div class="w-16 h-16 bg-warning/10 rounded-xl flex items-center justify-center mb-4">
                            <i class="fas fa-shield-alt text-warning text-3xl"></i>
                        </div>
                        <h3 class="text-xl font-bold mb-3">Compliance & Deliverability</h3>
                        <p class="text-base-content/70">
                            Using your Mail Client SMTP to ensure your emails reach the inbox.
                        </p>
                    </div>
                </div>

                <!-- Feature 6 -->
                <div class="card bg-base-100 shadow-xl border border-base-300 hover:shadow-2xl transition-all duration-300">
                    <div class="card-body p-8">
                        <div class="w-16 h-16 bg-error/10 rounded-xl flex items-center justify-center mb-4">
                            <i class="fas fa-plug text-error text-3xl"></i>
                        </div>
                        <h3 class="text-xl font-bold mb-3">CRM Integration</h3>
                        <p class="text-base-content/70">
                            Seamlessly integrates with popular CRMs like Salesforce, HubSpot, and Zoho.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </div>







      <!-- =============================================== -->
        <!-- START: FINAL CALL TO ACTION (CTA) SECTION      -->
        <!-- =============================================== -->
        <div class="px-4 py-10 md:py-28 bg-base-100 relative overflow-hidden">
          <!-- Left Side Graphics -->
          <div class="absolute left-0 top-1/2 transform -translate-y-1/2 opacity-30 hidden lg:block">
            <div class="flex flex-col items-center space-y-8 pl-8">
              <!-- AI Brain Icon -->
              <div class="w-20 h-20 rounded-full bg-primary/20 flex items-center justify-center">
                <svg class="w-12 h-12 text-primary" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-2 15l-5-5 1.41-1.41L10 14.17l7.59-7.59L19 8l-9 9z"/>
                </svg>
              </div>
              <!-- Email Icon -->
              <div class="w-16 h-16 rounded-lg bg-secondary/20 flex items-center justify-center rotate-12">
                <svg class="w-10 h-10 text-secondary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/>
                </svg>
              </div>
              <!-- Target Icon -->
              <div class="w-14 h-14 rounded-full bg-accent/20 flex items-center justify-center -rotate-12">
                <svg class="w-8 h-8 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 2l3.09 6.26L22 9l-5 4.87L18.18 22 12 18.27 5.82 22 7 13.87 2 9l6.91-.74L12 2z"/>
                </svg>
              </div>
            </div>
          </div>

          <!-- Right Side Graphics -->
          <div class="absolute right-0 top-1/2 transform -translate-y-1/2 opacity-40 hidden lg:block">
            <div class="flex flex-col items-center space-y-8 pr-8">
              <!-- Analytics Chart Icon -->
              <div class="w-18 h-18 rounded-lg bg-info/20 flex items-center justify-center -rotate-6">
                <svg class="w-10 h-10 text-info" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"/>
                </svg>
              </div>
              <!-- Lightning/Speed Icon -->
              <div class="w-16 h-16 rounded-full bg-warning/20 flex items-center justify-center rotate-12">
                <svg class="w-10 h-10 text-warning" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M7 2v11h3v9l7-12h-4l4-8z"/>
                </svg>
              </div>
              <!-- Connection/Network Icon -->
              <div class="w-14 h-14 rounded-lg bg-success/20 flex items-center justify-center">
                <svg class="w-8 h-8 text-success" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"/>
                </svg>
              </div>
            </div>
          </div>

          <div class="container mx-auto px-6 py-20 text-center relative z-10">
            <h2 class="text-4xl md:text-5xl font-bold text-base-content">
              Ready to Stop Guessing and Start Converting?
            </h2>
            <p class="text-lg text-base-content/70 mt-4 mb-8 max-w-2xl mx-auto leading-relaxed">
              Transform your cold outreach from a numbers game into a science. Leverage AI to build real connections and see measurable results.
            </p>
            <div class="flex flex-col sm:flex-row justify-center items-center gap-4">
              <a href="#early-access" class="btn btn-primary btn-lg gap-2 shadow-lg hover:scale-105 transition-transform">
                Get Early Access Now
                <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H4" /></svg>
              </a>
              <a href="https://gataraai.zohobookings.com/#/ceo-call" class="btn btn-outline btn-lg gap-2">
                <i class="fas fa-play"></i>
                Book Demo
              </a>
            </div>
            <p class="text-sm text-base-content/50 mt-4">Join the program & shape the future of outreach.</p>
          </div>
        </div>
        <!-- =============================================== -->
        <!-- END: FINAL CALL TO ACTION (CTA) SECTION        -->
        <!-- =============================================== -->



    



        <!-- =============================================== -->
        <!-- START: FOOTER SECTION                          -->
        <!-- =============================================== -->
       
       <footer class="w-full px-[25px] sm:px-4 py-6 pt-[5vh] flex flex-col items-center gap-4 text-base text-gray-600 bg-base-100 pb-0 sm:pb-6">
        <!-- Social Icons -->
        <div class="flex items-center justify-center gap-6">
          <a href="https://gatara.org" target="_blank" class="hover:text-primary text-xl">
            <i class="fas fa-globe"></i>
          </a>
          <a href="https://www.linkedin.com/company/gatara-ai" target="_blank" class="hover:text-primary text-xl">
            <i class="fab fa-linkedin"></i>
          </a>
        </div>

        <!-- Footer Text -->
        <div class="text-center text-base text-lg">
          © 2025 <span class="font-semibold">GataraAI</span>, All rights reserved.
          <a href="mailto:info@gatara.org" class="ml-2 font-medium text-orange-500 hover:underline">Contact us</a>
        </div>
      </footer>

        <!-- =============================================== -->
        <!-- END: FOOTER SECTION                            -->
        <!-- =============================================== -->



























    </div>


    
  `}function Fs(){return`
    <div class="min-h-screen bg-base-200">
      <div class="container mx-auto px-1 sm:px-6 py-8">
        <div class="mb-8">
          <a href="#landing" class="btn btn-ghost gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back to Home
          </a>
        </div>
        
        <div id="user-section" class="max-w-2xl mx-auto">
          <div class="card bg-base-100 shadow-2xl">
            <div class="card-body p-8">
              <div class="text-center mb-8">
                <h1 class="text-4xl font-bold text-base-content mb-1">Get Started</h1>
                <h1 class="text-xl text-base-content mb-2 hormozi-gradient-text">Generate Hormozi-Style Headlines & Email Subjects for Free! ;)</h1>
                <p class="text-lg text-base-content/70">First, we need some basic information about you</p>
              </div>
              
              <form id="user-form" class="space-y-6">
                <div class="form-control">
                  <label class="label">
                    <span class="label-text font-semibold">Full Name</span>
                  </label>
                  <input type="text" id="name" name="name" class="input input-bordered input-lg" placeholder="Your Full Name" required>
                  <div id="name-error" class="label hidden">
                    <span class="label-text-alt text-error"></span>
                  </div>
                </div>
                
                <div class="form-control">
                  <label class="label">
                    <span class="label-text font-semibold">LinkedIn Profile Link</span>
                  </label>
                  <input type="url" id="linkedin" name="linkedin" class="input input-bordered input-lg" placeholder="https://linkedin.com/in/your-profile" required>
                  <div id="linkedin-error" class="label hidden">
                    <span class="label-text-alt text-error"></span>
                  </div>
                </div>
                
                <div class="form-control">
                  <label class="label">
                    <span class="label-text font-semibold">Business Email</span>
                  </label>
                  <input type="email" id="email" name="email" class="input input-bordered input-lg"  placeholder="Your Business Email" required>
                  <div id="email-error" class="label hidden">
                    <span class="label-text-alt text-error"></span>
                  </div>
                  <div class="label">
                    <span class="label-text-alt text-base-content/60">Gmail/Outlook addresses are not accepted for business use</span>
                  </div>
                </div>
                
                <button type="submit" class="btn btn-primary btn-lg w-full">
                  Continue
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </button>
              </form>
            </div>
          </div>
        </div>

        <div id="ai-section" class="max-w-3xl mx-auto hidden">
          <div class="card bg-base-100 shadow-2xl">
            <div class="card-body p-8">
              <div class="text-center mb-8">
                <h1 class="text-4xl font-bold text-base-content mb-4">Generate Hormozi-style headlines and subjects for your cold outreach!</h1>
                <div class="alert alert-warning">
                  <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                  </svg>
                  <span class="font-semibold">⚠️ You only got one shot, use it wisely!</span>
                </div>
              </div>
              
              <form id="ai-form" class="space-y-6">
                <div class="form-control">
                  <label class="label">
                    <span class="label-text font-semibold">Email Content</span>
                  </label>
                  <textarea id="email_content" name="email_content" class="textarea textarea-bordered textarea-lg h-32" placeholder="INSERT EMAIL BODY HERE" required></textarea>
                </div>
                
                <div class="form-control">
                  <label class="label">
                    <span class="label-text font-semibold">Target Audience</span>
                  </label>
                  <input type="text" id="target_audience" name="target_audience" class="input input-bordered input-lg" placeholder="e.g., B2B SaaS founders, 51–200 employees" required>
                </div>
                
                <div class="form-control">
                  <label class="label">
                    <span class="label-text font-semibold">Tone of Voice</span>
                  </label>
                  <input type="text" id="tone_of_voice" name="tone_of_voice" class="input input-bordered input-lg" placeholder="e.g., like Hormozi meets cold email pro" required>
                </div>
                
                <div class="form-control">
                  <label class="label">
                    <span class="label-text font-semibold">Main Pain Point</span>
                  </label>
                  <textarea id="main_pain" name="main_pain" class="textarea textarea-bordered textarea-lg h-24" placeholder="Manual cold outreach is time-consuming, lack of personalization, doesn't scale" required></textarea>
                </div>
                
                <div class="form-control">
                  <label class="label">
                    <span class="label-text font-semibold">Outcome We Promise</span>
                  </label>
                  <input type="text" id="outcome" name="outcome" class="input input-bordered input-lg" placeholder="Get more replies and convert more." required>
                </div>
                
                <button type="submit" class="btn btn-primary btn-lg w-full">
                  <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                  Generate Headlines
                </button>
              </form>
            </div>
          </div>
        </div>

        <div id="loader-section" class="max-w-2xl mx-auto hidden">
          <div class="card bg-base-100 shadow-2xl">
            <div class="card-body p-12 text-center">
              <!-- loder -->
              <div class="flex-col gap-4 w-full flex items-center justify-center pb-4">
                <div
                  class="w-20 h-20 border-4 border-transparent text-blue-400 text-4xl animate-spin flex items-center justify-center border-t-blue-400 rounded-full"
                >
                  <div
                    class="w-16 h-16 border-4 border-transparent text-red-400 text-2xl animate-spin flex items-center justify-center border-t-red-400 rounded-full"
                  ></div>
                </div>
              </div>

              <h2 class="text-3xl font-bold text-base-content mb-4">Bear with me for a minute...</h2>
              <p class="text-lg text-base-content/70 leading-relaxed">I'm not a normal AI, and I focus on results and it will be valuable for you, so I will take time to think ;)</p>
            </div>
          </div>
        </div>

        <div id="result-section" class="max-w-4xl mx-auto hidden">
          <!-- Results will be populated here -->
        </div>
      </div>
    </div>
  `}function $s(){return`
    <div class="min-h-screen bg-base-200">
      <div class="container mx-auto px-1 sm:px-6 py-8">
        <div class="mb-8">
          <a href="#landing" class="btn btn-ghost gap-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            Back to Home
          </a>
        </div>
        
        <div class="w-full max-w-4xl mx-auto flex flex-col justify-center">
          <!-- Welcome Screen -->
          <div id="welcome-screen" class="bg-base-100 rounded-xl shadow-lg p-6 md:p-10 flex flex-col items-center justify-center text-center">
            <div class="mb-8">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <h1 class="text-4xl md:text-5xl font-bold text-base-content mb-4">Get Exclusive Early Access</h1>
            <p class="text-lg md:text-xl text-base-content/80 leading-relaxed mb-8 max-w-2xl mx-auto">
              Join our VIP list to be among the first to <span class="font-semibold text-primary">10x your outbound pipeline</span> with AI-powered, personalized cold emails — no manual work required.
            </p>
            <div class="space-y-4 w-full max-w-xs">
              <button id="start-form" class="btn btn-primary btn-lg w-full text-lg transform transition-transform hover:scale-[1.02] active:scale-95">
                Apply Now
                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 ml-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
                </svg>
              </button>
              <p class="text-sm text-base-content/60">Takes just 2 minutes</p>
            </div>
            <div class="mt-8 flex items-center space-x-4">
              <div class="flex -space-x-2">
                <div class="h-8 w-8 rounded-full bg-primary/20 border-2 border-base-100"></div>
                <div class="h-8 w-8 rounded-full bg-primary/30 border-2 border-base-100"></div>
                <div class="h-8 w-8 rounded-full bg-primary/40 border-2 border-base-100"></div>
              </div>
              <p class="text-sm text-base-content/60">Join VibeReach early adopters</p>
            </div>
          </div>

          <!-- Multi-step Form -->
          <div id="form-container" class="bg-base-100 rounded-xl shadow-lg hidden">
            <!-- Progress Bar -->
            <div class="px-6 pt-6 sticky top-0 bg-base-100 z-10 border-b border-base-200">
              <div class="flex justify-between items-center mb-2">
                <span class="text-sm font-medium text-base-content/70">Step  <span id="progress-text">1</span> of 13</span>
                <span id="progress-percent" class="text-sm font-medium text-primary">8%</span>
              </div>
              <div class="w-full bg-base-200 rounded-full h-2.5 mb-4">
                <div id="progress-bar" class="bg-primary h-2.5 rounded-full transition-all duration-300" style="width: 7.7%"></div>
              </div>
            </div>

            <div class="px-6 pb-8">
              <form id="early-access-form" class="flex flex-col">
                <!-- Step 1: Name -->
                <div class="form-step active" data-step="1">
                  <div class="py-8 md:py-12 text-center">
                    <h2 class="text-3xl md:text-4xl font-bold text-base-content mb-3">What's your name?</h2>
                    <p class="text-base-content/60 max-w-md mx-auto">We'll use this to personalize your experience</p>
                  </div>
                  <div class="max-w-md mx-auto">
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                      <div class="form-control">
                        <label class="label">
                          <span class="label-text text-base-content/70">First Name</span>
                        </label>
                        <div class="relative">
                          <input type="text" name="firstName" class="input input-bordered w-full text-lg pl-10" placeholder="John" required>
                          <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 absolute left-3 top-3.5 text-base-content/40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                          </svg>
                        </div>
                      </div>
                      <div class="form-control">
                        <label class="label">
                          <span class="label-text text-base-content/70">Last Name</span>
                        </label>
                        <input type="text" name="lastName" class="input input-bordered w-full text-lg" placeholder="Doe" required>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Step 2: Business Email -->
                <div class="form-step" data-step="2">
                  <div class="py-8 md:py-12 text-center">
                    <h2 class="text-3xl md:text-4xl font-bold text-base-content mb-3">What's your business email?</h2>
                    <p class="text-base-content/60 max-w-md mx-auto">We'll send your early access invite here</p>
                  </div>
                  <div class="max-w-md mx-auto">
                    <div class="form-control">
                      <label class="label">
                        <span class="label-text text-base-content/70">Email Address</span>
                      </label>
                      <div class="relative">
                        <input type="email" name="email" class="input input-bordered w-full text-lg pl-10" placeholder="john@company.com" required>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 absolute left-3 top-3.5 text-base-content/40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                        </svg>
                      </div>
                      <label class="label">
                        <span class="label-text-alt text-base-content/50">Please use your business email address</span>
                      </label>
                    </div>
                  </div>
                </div>

                <!-- Step 3: Position -->
                <div class="form-step" data-step="3">
                  <div class="py-8 md:py-12 text-center">
                    <h2 class="text-3xl md:text-4xl font-bold text-base-content mb-3">What's your position?</h2>
                    <p class="text-base-content/60 max-w-md mx-auto">Helps us tailor the experience to your role</p>
                  </div>
                  <div class="max-w-md mx-auto">
                    <div class="form-control">
                      <label class="label">
                        <span class="label-text text-base-content/70">Your Role</span>
                      </label>
                      <div class="relative">
                        <input type="text" name="position" class="input input-bordered w-full text-lg pl-10" placeholder="e.g., Sales Director, Marketing Manager" required>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 absolute left-3 top-3.5 text-base-content/40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2-2v2m8 0H8m8 0v2a2 2 0 01-2 2H10a2 2 0 01-2-2V6" />
                        </svg>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Step 4: LinkedIn -->
                <div class="form-step" data-step="4">
                  <div class="py-8 md:py-12 text-center">
                    <h2 class="text-3xl md:text-4xl font-bold text-base-content mb-3">What's your LinkedIn profile?</h2>
                    <p class="text-base-content/60 max-w-md mx-auto">Helps us verify you're a real professional</p>
                  </div>
                  <div class="max-w-md mx-auto">
                    <div class="form-control">
                      <label class="label">
                        <span class="label-text text-base-content/70">LinkedIn URL</span>
                      </label>
                      <div class="relative">
                        <input type="url" name="linkedin" class="input input-bordered w-full text-lg pl-10" placeholder="https://linkedin.com/in/your-profile" required>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 absolute left-3 top-3.5 text-base-content/40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.828 10.172a4 4 0 00-5.656 0l-4 4a4 4 0 105.656 5.656l1.102-1.101m-.758-4.899a4 4 0 005.656 0l4-4a4 4 0 00-5.656-5.656l-1.1 1.1" />
                        </svg>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Step 5: Company Name -->
                <div class="form-step" data-step="5">
                  <div class="py-8 md:py-12 text-center">
                    <h2 class="text-3xl md:text-4xl font-bold text-base-content mb-3">What company do you work for?</h2>
                    <p class="text-base-content/60 max-w-md mx-auto">Helps us understand your needs better</p>
                  </div>
                  <div class="max-w-md mx-auto">
                    <div class="form-control">
                      <label class="label">
                        <span class="label-text text-base-content/70">Company Name</span>
                      </label>
                      <div class="relative">
                        <input type="text" name="company" class="input input-bordered w-full text-lg pl-10" placeholder="Acme Inc." required>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 absolute left-3 top-3.5 text-base-content/40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                        </svg>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Step 6: Company Website -->
                <div class="form-step" data-step="6">
                  <div class="py-8 md:py-12 text-center">
                    <h2 class="text-3xl md:text-4xl font-bold text-base-content mb-3">What's your company website?</h2>
                    <p class="text-base-content/60 max-w-md mx-auto">We'll research your company to personalize your demo</p>
                  </div>
                  <div class="max-w-md mx-auto">
                    <div class="form-control">
                      <label class="label">
                        <span class="label-text text-base-content/70">Website URL</span>
                      </label>
                      <div class="relative">
                        <input type="url" name="website" class="input input-bordered w-full text-lg pl-10" placeholder="https://yourcompany.com" required>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 absolute left-3 top-3.5 text-base-content/40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 12a9 9 0 01-9 9m9-9a9 9 0 00-9-9m9 9H3m9 9v-9m0-9v9m0 9c-5 0-9-4-9-9s4-9 9-9" />
                        </svg>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Step 7: Cold Outreach -->
                <div class="form-step" data-step="7">
                  <div class="py-8 md:py-12 text-center">
                    <h2 class="text-3xl md:text-4xl font-bold text-base-content mb-3">Do you currently run cold outreach campaigns?</h2>
                    <p class="text-base-content/60 max-w-md mx-auto">Helps us understand your current workflow</p>
                  </div>
                  <div class="max-w-md mx-auto space-y-3">
                    <div class="form-control">
                      <label class="label cursor-pointer justify-start gap-4 p-4 hover:bg-base-200 rounded-lg transition-colors">
                        <input type="radio" name="outreach" value="active" class="radio radio-primary" required>
                        <span class="label-text text-lg text-base-content">Yes – we're actively doing cold outreach</span>
                      </label>
                    </div>
                    <div class="form-control">
                      <label class="label cursor-pointer justify-start gap-4 p-4 hover:bg-base-200 rounded-lg transition-colors">
                        <input type="radio" name="outreach" value="soon" class="radio radio-primary" required>
                        <span class="label-text text-lg text-base-content">No – we want to start soon</span>
                      </label>
                    </div>
                    <div class="form-control">
                      <label class="label cursor-pointer justify-start gap-4 p-4 hover:bg-base-200 rounded-lg transition-colors">
                        <input type="radio" name="outreach" value="exploring" class="radio radio-primary" required>
                        <span class="label-text text-lg text-base-content">No – just exploring options</span>
                      </label>
                    </div>
                  </div>
                </div>

                <!-- Step 8: Automation -->
                <div class="form-step" data-step="8">
                  <div class="py-8 md:py-12 text-center">
                    <h2 class="text-3xl md:text-4xl font-bold text-base-content mb-3">Is your current cold outreach process automated?</h2>
                    <p class="text-base-content/60 max-w-md mx-auto">Helps us understand your current tech stack</p>
                  </div>
                  <div class="max-w-md mx-auto space-y-3">
                    <div class="form-control">
                      <label class="label cursor-pointer justify-start gap-4 p-4 hover:bg-base-200 rounded-lg transition-colors">
                        <input type="radio" name="automation" value="fully" class="radio radio-primary" required>
                        <span class="label-text text-lg text-base-content">Fully automated</span>
                      </label>
                    </div>
                    <div class="form-control">
                      <label class="label cursor-pointer justify-start gap-4 p-4 hover:bg-base-200 rounded-lg transition-colors">
                        <input type="radio" name="automation" value="partially" class="radio radio-primary" required>
                        <span class="label-text text-lg text-base-content">Partially automated</span>
                      </label>
                    </div>
                    <div class="form-control">
                      <label class="label cursor-pointer justify-start gap-4 p-4 hover:bg-base-200 rounded-lg transition-colors">
                        <input type="radio" name="automation" value="manual" class="radio radio-primary" required>
                        <span class="label-text text-lg text-base-content">Completely manual</span>
                      </label>
                    </div>
                    <div class="form-control">
                      <label class="label cursor-pointer justify-start gap-4 p-4 hover:bg-base-200 rounded-lg transition-colors">
                        <input type="radio" name="automation" value="none" class="radio radio-primary" required>
                        <span class="label-text text-lg text-base-content">Not doing outreach yet</span>
                      </label>
                    </div>
                  </div>
                </div>

                <!-- Step 9: Tools -->
                <div class="form-step" data-step="9">
                  <div class="py-8 md:py-12 text-center">
                    <h2 class="text-3xl md:text-4xl font-bold text-base-content mb-3">What automation tools are you currently using for outreach?</h2>
                    <p class="text-base-content/60 max-w-md mx-auto">Helps us integrate with your existing workflow</p>
                  </div>
                  <div class="max-w-md mx-auto">
                    <div class="form-control">
                      <label class="label">
                        <span class="label-text text-base-content/70">Tools (if any)</span>
                      </label>
                      <div class="relative">
                        <input type="text" name="tools" class="input input-bordered w-full text-lg pl-10" placeholder="e.g., Outreach, SalesLoft, Apollo, or None" required>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 absolute left-3 top-3.5 text-base-content/40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                        </svg>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Step 10: Challenge -->
                <div class="form-step" data-step="10">
                  <div class="py-8 md:py-12 text-center">
                    <h2 class="text-3xl md:text-4xl font-bold text-base-content mb-3">What's your biggest challenge with your current outreach workflow?</h2>
                    <p class="text-base-content/60 max-w-md mx-auto">We'll focus on solving this first for you</p>
                  </div>
                  <div class="max-w-md mx-auto">
                    <div class="form-control">
                      <label class="label">
                        <span class="label-text text-base-content/70">Your Challenge</span>
                      </label>
                      <div class="relative">
                       <textarea 
                          name="challenge" 
                          class="textarea textarea-bordered w-full text-lg pl-10 min-h-[100px]" 
                          placeholder="Manual cold outreach is time-consuming, lack of personalization, doesn't scale" 
                          required
                        ></textarea>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 absolute left-3 top-3.5 text-base-content/40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                        </svg>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Step 11: Volume -->
                <div class="form-step" data-step="11">
                  <div class="py-8 md:py-12 text-center">
                    <h2 class="text-3xl md:text-4xl font-bold text-base-content mb-3">How many leads do you typically reach out to per month?</h2>
                    <p class="text-base-content/60 max-w-md mx-auto">Helps us understand your scale needs</p>
                  </div>
                  <div class="max-w-md mx-auto space-y-3">
                    <div class="form-control">
                      <label class="label cursor-pointer justify-start gap-4 p-4 hover:bg-base-200 rounded-lg transition-colors">
                        <input type="radio" name="volume" value="<100" class="radio radio-primary" required>
                        <span class="label-text text-lg text-base-content">Less than 100</span>
                      </label>
                    </div>
                    <div class="form-control">
                      <label class="label cursor-pointer justify-start gap-4 p-4 hover:bg-base-200 rounded-lg transition-colors">
                        <input type="radio" name="volume" value="100-500" class="radio radio-primary" required>
                        <span class="label-text text-lg text-base-content">100–500</span>
                      </label>
                    </div>
                    <div class="form-control">
                      <label class="label cursor-pointer justify-start gap-4 p-4 hover:bg-base-200 rounded-lg transition-colors">
                        <input type="radio" name="volume" value="500-2000" class="radio radio-primary" required>
                        <span class="label-text text-lg text-base-content">500–2,000</span>
                      </label>
                    </div>
                    <div class="form-control">
                      <label class="label cursor-pointer justify-start gap-4 p-4 hover:bg-base-200 rounded-lg transition-colors">
                        <input type="radio" name="volume" value="2000+" class="radio radio-primary" required>
                        <span class="label-text text-lg text-base-content">More than 2,000</span>
                      </label>
                    </div>
                  </div>
                </div>

                <!-- Step 12: CRM -->
                <div class="form-step" data-step="12">
                  <div class="py-8 md:py-12 text-center">
                    <h2 class="text-3xl md:text-4xl font-bold text-base-content mb-3">What CRM software do you use?</h2>
                    <p class="text-base-content/60 max-w-md mx-auto">We'll prioritize integrations with your CRM</p>
                  </div>
                  <div class="max-w-md mx-auto">
                    <div class="form-control">
                      <label class="label">
                        <span class="label-text text-base-content/70">CRM Name</span>
                      </label>
                      <div class="relative">
                        <input type="text" name="crm" class="input input-bordered w-full text-lg pl-10" placeholder="e.g., Salesforce, HubSpot, Pipedrive, or None" required>
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 absolute left-3 top-3.5 text-base-content/40" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                        </svg>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Step 13: Chat -->
                <div class="form-step" data-step="13">
                  <div class="py-8 md:py-12 text-center">
                    <h2 class="text-3xl md:text-4xl font-bold text-base-content mb-3">Want priority access?</h2>
                    <p class="text-base-content/60 max-w-md mx-auto">A quick 15-min chat jumps you to the front of the line</p>
                  </div>
                  <div class="max-w-md mx-auto space-y-3">
                    <div class="form-control">
                      <label class="label cursor-pointer justify-start gap-4 p-4 hover:bg-base-200 rounded-lg transition-colors">
                        <input type="radio" name="chat" value="yes" class="radio radio-primary" required>
                        <span class="label-text text-lg text-base-content">Yes, book me for a quick chat</span>
                      </label>
                    </div>
                    <div class="form-control">
                      <label class="label cursor-pointer justify-start gap-4 p-4 hover:bg-base-200 rounded-lg transition-colors">
                        <input type="radio" name="chat" value="no" class="radio radio-primary" required>
                        <span class="label-text text-lg text-base-content">No thanks, just add me to the waitlist</span>
                      </label>
                    </div>
                  </div>
                </div>

                <!-- Navigation Buttons -->
                <div class="flex justify-between items-center mt-12 max-w-md mx-auto w-full">
                  <button type="button" id="prev-btn" class="btn btn-ghost text-primary hover:bg-primary/10 gap-2" disabled>
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                    </svg>
                    Previous
                  </button>
                  <div class="flex items-center gap-2 text-sm text-base-content/50">
                    <span id="current-step">1</span>
                    <span>/</span>
                    <span>13</span>
                  </div>
                  <button type="button" id="next-btn" class="btn btn-primary gap-2">
                    Next
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 7l5 5m0 0l-5 5m5-5H6" />
                    </svg>
                  </button>
                  <button type="submit" id="submit-btn" class="btn btn-primary gap-2 hidden">
                    Submit Application
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                  </button>
                </div>
              </form>
            </div>
          </div>

          <!-- Thank You Screen -->
          <div id="thank-you-screen" class="bg-base-100 rounded-xl shadow-lg p-8 md:p-12 hidden">
            <div class="text-center max-w-2xl mx-auto">
              <div class="mb-8">
                <svg xmlns="http://www.w3.org/2000/svg" class="h-16 w-16 mx-auto text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h1 class="text-3xl md:text-4xl font-bold text-base-content mb-4">You're on the list!</h1>
              <p class="text-lg text-base-content/80 leading-relaxed mb-8">
                Thanks for applying for early access to VibeOutreach. We'll review your application and get back to you soon with your exclusive invite.
              </p>
              <div class="space-y-4">
                <div id="chat-option" class="hidden">
                  <p class="text-base-content/70 mb-4">Want to skip the line?</p>
                  <a href="https://gataraai.zohobookings.com/#/ceo-call" class="btn btn-secondary btn-lg w-full max-w-xs">
                    Book a quick 15-min chat
                  </a>
                </div>
                <div class="pt-8">
                  <p class="text-sm text-base-content/60">In the meantime, follow us on <a href="https://linkedin.com/company/omar-gatara" class="link link-primary">LinkedIn</a> for updates.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `}function ht(){return{async:!1,breaks:!1,extensions:null,gfm:!0,hooks:null,pedantic:!1,renderer:null,silent:!1,tokenizer:null,walkTokens:null}}var te=ht();function os(s){te=s}var ye={exec:()=>null};function b(s,e=""){let t=typeof s=="string"?s:s.source;const a={replace:(n,i)=>{let c=typeof i=="string"?i:i.source;return c=c.replace(P.caret,"$1"),t=t.replace(n,c),a},getRegex:()=>new RegExp(t,e)};return a}var P={codeRemoveIndent:/^(?: {1,4}| {0,3}\t)/gm,outputLinkReplace:/\\([\[\]])/g,indentCodeCompensation:/^(\s+)(?:```)/,beginningSpace:/^\s+/,endingHash:/#$/,startingSpaceChar:/^ /,endingSpaceChar:/ $/,nonSpaceChar:/[^ ]/,newLineCharGlobal:/\n/g,tabCharGlobal:/\t/g,multipleSpaceGlobal:/\s+/g,blankLine:/^[ \t]*$/,doubleBlankLine:/\n[ \t]*\n[ \t]*$/,blockquoteStart:/^ {0,3}>/,blockquoteSetextReplace:/\n {0,3}((?:=+|-+) *)(?=\n|$)/g,blockquoteSetextReplace2:/^ {0,3}>[ \t]?/gm,listReplaceTabs:/^\t+/,listReplaceNesting:/^ {1,4}(?=( {4})*[^ ])/g,listIsTask:/^\[[ xX]\] /,listReplaceTask:/^\[[ xX]\] +/,anyLine:/\n.*\n/,hrefBrackets:/^<(.*)>$/,tableDelimiter:/[:|]/,tableAlignChars:/^\||\| *$/g,tableRowBlankLine:/\n[ \t]*$/,tableAlignRight:/^ *-+: *$/,tableAlignCenter:/^ *:-+: *$/,tableAlignLeft:/^ *:-+ *$/,startATag:/^<a /i,endATag:/^<\/a>/i,startPreScriptTag:/^<(pre|code|kbd|script)(\s|>)/i,endPreScriptTag:/^<\/(pre|code|kbd|script)(\s|>)/i,startAngleBracket:/^</,endAngleBracket:/>$/,pedanticHrefTitle:/^([^'"]*[^\s])\s+(['"])(.*)\2/,unicodeAlphaNumeric:/[\p{L}\p{N}]/u,escapeTest:/[&<>"']/,escapeReplace:/[&<>"']/g,escapeTestNoEncode:/[<>"']|&(?!(#\d{1,7}|#[Xx][a-fA-F0-9]{1,6}|\w+);)/,escapeReplaceNoEncode:/[<>"']|&(?!(#\d{1,7}|#[Xx][a-fA-F0-9]{1,6}|\w+);)/g,unescapeTest:/&(#(?:\d+)|(?:#x[0-9A-Fa-f]+)|(?:\w+));?/ig,caret:/(^|[^\[])\^/g,percentDecode:/%25/g,findPipe:/\|/g,splitPipe:/ \|/,slashPipe:/\\\|/g,carriageReturn:/\r\n|\r/g,spaceLine:/^ +$/gm,notSpaceStart:/^\S*/,endingNewline:/\n$/,listItemRegex:s=>new RegExp(`^( {0,3}${s})((?:[	 ][^\\n]*)?(?:\\n|$))`),nextBulletRegex:s=>new RegExp(`^ {0,${Math.min(3,s-1)}}(?:[*+-]|\\d{1,9}[.)])((?:[ 	][^\\n]*)?(?:\\n|$))`),hrRegex:s=>new RegExp(`^ {0,${Math.min(3,s-1)}}((?:- *){3,}|(?:_ *){3,}|(?:\\* *){3,})(?:\\n+|$)`),fencesBeginRegex:s=>new RegExp(`^ {0,${Math.min(3,s-1)}}(?:\`\`\`|~~~)`),headingBeginRegex:s=>new RegExp(`^ {0,${Math.min(3,s-1)}}#`),htmlBeginRegex:s=>new RegExp(`^ {0,${Math.min(3,s-1)}}<(?:[a-z].*>|!--)`,"i")},Us=/^(?:[ \t]*(?:\n|$))+/,Gs=/^((?: {4}| {0,3}\t)[^\n]+(?:\n(?:[ \t]*(?:\n|$))*)?)+/,qs=/^ {0,3}(`{3,}(?=[^`\n]*(?:\n|$))|~{3,})([^\n]*)(?:\n|$)(?:|([\s\S]*?)(?:\n|$))(?: {0,3}\1[~`]* *(?=\n|$)|$)/,ke=/^ {0,3}((?:-[\t ]*){3,}|(?:_[ \t]*){3,}|(?:\*[ \t]*){3,})(?:\n+|$)/,Ws=/^ {0,3}(#{1,6})(?=\s|$)(.*)(?:\n+|$)/,mt=/(?:[*+-]|\d{1,9}[.)])/,cs=/^(?!bull |blockCode|fences|blockquote|heading|html|table)((?:.|\n(?!\s*?\n|bull |blockCode|fences|blockquote|heading|html|table))+?)\n {0,3}(=+|-+) *(?:\n+|$)/,ds=b(cs).replace(/bull/g,mt).replace(/blockCode/g,/(?: {4}| {0,3}\t)/).replace(/fences/g,/ {0,3}(?:`{3,}|~{3,})/).replace(/blockquote/g,/ {0,3}>/).replace(/heading/g,/ {0,3}#{1,6}/).replace(/html/g,/ {0,3}<[^\n>]+>\n/).replace(/\|table/g,"").getRegex(),Vs=b(cs).replace(/bull/g,mt).replace(/blockCode/g,/(?: {4}| {0,3}\t)/).replace(/fences/g,/ {0,3}(?:`{3,}|~{3,})/).replace(/blockquote/g,/ {0,3}>/).replace(/heading/g,/ {0,3}#{1,6}/).replace(/html/g,/ {0,3}<[^\n>]+>\n/).replace(/table/g,/ {0,3}\|?(?:[:\- ]*\|)+[\:\- ]*\n/).getRegex(),ft=/^([^\n]+(?:\n(?!hr|heading|lheading|blockquote|fences|list|html|table| +\n)[^\n]+)*)/,Ys=/^[^\n]+/,gt=/(?!\s*\])(?:\\.|[^\[\]\\])+/,Zs=b(/^ {0,3}\[(label)\]: *(?:\n[ \t]*)?([^<\s][^\s]*|<.*?>)(?:(?: +(?:\n[ \t]*)?| *\n[ \t]*)(title))? *(?:\n+|$)/).replace("label",gt).replace("title",/(?:"(?:\\"?|[^"\\])*"|'[^'\n]*(?:\n[^'\n]+)*\n?'|\([^()]*\))/).getRegex(),Xs=b(/^( {0,3}bull)([ \t][^\n]+?)?(?:\n|$)/).replace(/bull/g,mt).getRegex(),He="address|article|aside|base|basefont|blockquote|body|caption|center|col|colgroup|dd|details|dialog|dir|div|dl|dt|fieldset|figcaption|figure|footer|form|frame|frameset|h[1-6]|head|header|hr|html|iframe|legend|li|link|main|menu|menuitem|meta|nav|noframes|ol|optgroup|option|p|param|search|section|summary|table|tbody|td|tfoot|th|thead|title|tr|track|ul",xt=/<!--(?:-?>|[\s\S]*?(?:-->|$))/,Ks=b("^ {0,3}(?:<(script|pre|style|textarea)[\\s>][\\s\\S]*?(?:</\\1>[^\\n]*\\n+|$)|comment[^\\n]*(\\n+|$)|<\\?[\\s\\S]*?(?:\\?>\\n*|$)|<![A-Z][\\s\\S]*?(?:>\\n*|$)|<!\\[CDATA\\[[\\s\\S]*?(?:\\]\\]>\\n*|$)|</?(tag)(?: +|\\n|/?>)[\\s\\S]*?(?:(?:\\n[ 	]*)+\\n|$)|<(?!script|pre|style|textarea)([a-z][\\w-]*)(?:attribute)*? */?>(?=[ \\t]*(?:\\n|$))[\\s\\S]*?(?:(?:\\n[ 	]*)+\\n|$)|</(?!script|pre|style|textarea)[a-z][\\w-]*\\s*>(?=[ \\t]*(?:\\n|$))[\\s\\S]*?(?:(?:\\n[ 	]*)+\\n|$))","i").replace("comment",xt).replace("tag",He).replace("attribute",/ +[a-zA-Z:_][\w.:-]*(?: *= *"[^"\n]*"| *= *'[^'\n]*'| *= *[^\s"'=<>`]+)?/).getRegex(),ps=b(ft).replace("hr",ke).replace("heading"," {0,3}#{1,6}(?:\\s|$)").replace("|lheading","").replace("|table","").replace("blockquote"," {0,3}>").replace("fences"," {0,3}(?:`{3,}(?=[^`\\n]*\\n)|~{3,})[^\\n]*\\n").replace("list"," {0,3}(?:[*+-]|1[.)]) ").replace("html","</?(?:tag)(?: +|\\n|/?>)|<(?:script|pre|style|textarea|!--)").replace("tag",He).getRegex(),Js=b(/^( {0,3}> ?(paragraph|[^\n]*)(?:\n|$))+/).replace("paragraph",ps).getRegex(),bt={blockquote:Js,code:Gs,def:Zs,fences:qs,heading:Ws,hr:ke,html:Ks,lheading:ds,list:Xs,newline:Us,paragraph:ps,table:ye,text:Ys},Yt=b("^ *([^\\n ].*)\\n {0,3}((?:\\| *)?:?-+:? *(?:\\| *:?-+:? *)*(?:\\| *)?)(?:\\n((?:(?! *\\n|hr|heading|blockquote|code|fences|list|html).*(?:\\n|$))*)\\n*|$)").replace("hr",ke).replace("heading"," {0,3}#{1,6}(?:\\s|$)").replace("blockquote"," {0,3}>").replace("code","(?: {4}| {0,3}	)[^\\n]").replace("fences"," {0,3}(?:`{3,}(?=[^`\\n]*\\n)|~{3,})[^\\n]*\\n").replace("list"," {0,3}(?:[*+-]|1[.)]) ").replace("html","</?(?:tag)(?: +|\\n|/?>)|<(?:script|pre|style|textarea|!--)").replace("tag",He).getRegex(),Qs={...bt,lheading:Vs,table:Yt,paragraph:b(ft).replace("hr",ke).replace("heading"," {0,3}#{1,6}(?:\\s|$)").replace("|lheading","").replace("table",Yt).replace("blockquote"," {0,3}>").replace("fences"," {0,3}(?:`{3,}(?=[^`\\n]*\\n)|~{3,})[^\\n]*\\n").replace("list"," {0,3}(?:[*+-]|1[.)]) ").replace("html","</?(?:tag)(?: +|\\n|/?>)|<(?:script|pre|style|textarea|!--)").replace("tag",He).getRegex()},ea={...bt,html:b(`^ *(?:comment *(?:\\n|\\s*$)|<(tag)[\\s\\S]+?</\\1> *(?:\\n{2,}|\\s*$)|<tag(?:"[^"]*"|'[^']*'|\\s[^'"/>\\s]*)*?/?> *(?:\\n{2,}|\\s*$))`).replace("comment",xt).replace(/tag/g,"(?!(?:a|em|strong|small|s|cite|q|dfn|abbr|data|time|code|var|samp|kbd|sub|sup|i|b|u|mark|ruby|rt|rp|bdi|bdo|span|br|wbr|ins|del|img)\\b)\\w+(?!:|[^\\w\\s@]*@)\\b").getRegex(),def:/^ *\[([^\]]+)\]: *<?([^\s>]+)>?(?: +(["(][^\n]+[")]))? *(?:\n+|$)/,heading:/^(#{1,6})(.*)(?:\n+|$)/,fences:ye,lheading:/^(.+?)\n {0,3}(=+|-+) *(?:\n+|$)/,paragraph:b(ft).replace("hr",ke).replace("heading",` *#{1,6} *[^
]`).replace("lheading",ds).replace("|table","").replace("blockquote"," {0,3}>").replace("|fences","").replace("|list","").replace("|html","").replace("|tag","").getRegex()},ta=/^\\([!"#$%&'()*+,\-./:;<=>?@\[\]\\^_`{|}~])/,sa=/^(`+)([^`]|[^`][\s\S]*?[^`])\1(?!`)/,us=/^( {2,}|\\)\n(?!\s*$)/,aa=/^(`+|[^`])(?:(?= {2,}\n)|[\s\S]*?(?:(?=[\\<!\[`*_]|\b_|$)|[^ ](?= {2,}\n)))/,Fe=/[\p{P}\p{S}]/u,vt=/[\s\p{P}\p{S}]/u,hs=/[^\s\p{P}\p{S}]/u,na=b(/^((?![*_])punctSpace)/,"u").replace(/punctSpace/g,vt).getRegex(),ms=/(?!~)[\p{P}\p{S}]/u,ia=/(?!~)[\s\p{P}\p{S}]/u,ra=/(?:[^\s\p{P}\p{S}]|~)/u,la=/\[[^[\]]*?\]\((?:\\.|[^\\\(\)]|\((?:\\.|[^\\\(\)])*\))*\)|`[^`]*?`|<[^<>]*?>/g,fs=/^(?:\*+(?:((?!\*)punct)|[^\s*]))|^_+(?:((?!_)punct)|([^\s_]))/,oa=b(fs,"u").replace(/punct/g,Fe).getRegex(),ca=b(fs,"u").replace(/punct/g,ms).getRegex(),gs="^[^_*]*?__[^_*]*?\\*[^_*]*?(?=__)|[^*]+(?=[^*])|(?!\\*)punct(\\*+)(?=[\\s]|$)|notPunctSpace(\\*+)(?!\\*)(?=punctSpace|$)|(?!\\*)punctSpace(\\*+)(?=notPunctSpace)|[\\s](\\*+)(?!\\*)(?=punct)|(?!\\*)punct(\\*+)(?!\\*)(?=punct)|notPunctSpace(\\*+)(?=notPunctSpace)",da=b(gs,"gu").replace(/notPunctSpace/g,hs).replace(/punctSpace/g,vt).replace(/punct/g,Fe).getRegex(),pa=b(gs,"gu").replace(/notPunctSpace/g,ra).replace(/punctSpace/g,ia).replace(/punct/g,ms).getRegex(),ua=b("^[^_*]*?\\*\\*[^_*]*?_[^_*]*?(?=\\*\\*)|[^_]+(?=[^_])|(?!_)punct(_+)(?=[\\s]|$)|notPunctSpace(_+)(?!_)(?=punctSpace|$)|(?!_)punctSpace(_+)(?=notPunctSpace)|[\\s](_+)(?!_)(?=punct)|(?!_)punct(_+)(?!_)(?=punct)","gu").replace(/notPunctSpace/g,hs).replace(/punctSpace/g,vt).replace(/punct/g,Fe).getRegex(),ha=b(/\\(punct)/,"gu").replace(/punct/g,Fe).getRegex(),ma=b(/^<(scheme:[^\s\x00-\x1f<>]*|email)>/).replace("scheme",/[a-zA-Z][a-zA-Z0-9+.-]{1,31}/).replace("email",/[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+(@)[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?(?:\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)+(?![-_])/).getRegex(),fa=b(xt).replace("(?:-->|$)","-->").getRegex(),ga=b("^comment|^</[a-zA-Z][\\w:-]*\\s*>|^<[a-zA-Z][\\w-]*(?:attribute)*?\\s*/?>|^<\\?[\\s\\S]*?\\?>|^<![a-zA-Z]+\\s[\\s\\S]*?>|^<!\\[CDATA\\[[\\s\\S]*?\\]\\]>").replace("comment",fa).replace("attribute",/\s+[a-zA-Z:_][\w.:-]*(?:\s*=\s*"[^"]*"|\s*=\s*'[^']*'|\s*=\s*[^\s"'=<>`]+)?/).getRegex(),ze=/(?:\[(?:\\.|[^\[\]\\])*\]|\\.|`[^`]*`|[^\[\]\\`])*?/,xa=b(/^!?\[(label)\]\(\s*(href)(?:(?:[ \t]*(?:\n[ \t]*)?)(title))?\s*\)/).replace("label",ze).replace("href",/<(?:\\.|[^\n<>\\])+>|[^ \t\n\x00-\x1f]*/).replace("title",/"(?:\\"?|[^"\\])*"|'(?:\\'?|[^'\\])*'|\((?:\\\)?|[^)\\])*\)/).getRegex(),xs=b(/^!?\[(label)\]\[(ref)\]/).replace("label",ze).replace("ref",gt).getRegex(),bs=b(/^!?\[(ref)\](?:\[\])?/).replace("ref",gt).getRegex(),ba=b("reflink|nolink(?!\\()","g").replace("reflink",xs).replace("nolink",bs).getRegex(),wt={_backpedal:ye,anyPunctuation:ha,autolink:ma,blockSkip:la,br:us,code:sa,del:ye,emStrongLDelim:oa,emStrongRDelimAst:da,emStrongRDelimUnd:ua,escape:ta,link:xa,nolink:bs,punctuation:na,reflink:xs,reflinkSearch:ba,tag:ga,text:aa,url:ye},va={...wt,link:b(/^!?\[(label)\]\((.*?)\)/).replace("label",ze).getRegex(),reflink:b(/^!?\[(label)\]\s*\[([^\]]*)\]/).replace("label",ze).getRegex()},ot={...wt,emStrongRDelimAst:pa,emStrongLDelim:ca,url:b(/^((?:ftp|https?):\/\/|www\.)(?:[a-zA-Z0-9\-]+\.?)+[^\s<]*|^email/,"i").replace("email",/[A-Za-z0-9._+-]+(@)[a-zA-Z0-9-_]+(?:\.[a-zA-Z0-9-_]*[a-zA-Z0-9])+(?![-_])/).getRegex(),_backpedal:/(?:[^?!.,:;*_'"~()&]+|\([^)]*\)|&(?![a-zA-Z0-9]+;$)|[?!.,:;*_'"~)]+(?!$))+/,del:/^(~~?)(?=[^\s~])((?:\\.|[^\\])*?(?:\\.|[^\s~\\]))\1(?=[^~]|$)/,text:/^([`~]+|[^`~])(?:(?= {2,}\n)|(?=[a-zA-Z0-9.!#$%&'*+\/=?_`{\|}~-]+@)|[\s\S]*?(?:(?=[\\<!\[`*~_]|\b_|https?:\/\/|ftp:\/\/|www\.|$)|[^ ](?= {2,}\n)|[^a-zA-Z0-9.!#$%&'*+\/=?_`{\|}~-](?=[a-zA-Z0-9.!#$%&'*+\/=?_`{\|}~-]+@)))/},wa={...ot,br:b(us).replace("{2,}","*").getRegex(),text:b(ot.text).replace("\\b_","\\b_| {2,}\\n").replace(/\{2,\}/g,"*").getRegex()},Oe={normal:bt,gfm:Qs,pedantic:ea},me={normal:wt,gfm:ot,breaks:wa,pedantic:va},ya={"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"},Zt=s=>ya[s];function $(s,e){if(e){if(P.escapeTest.test(s))return s.replace(P.escapeReplace,Zt)}else if(P.escapeTestNoEncode.test(s))return s.replace(P.escapeReplaceNoEncode,Zt);return s}function Xt(s){try{s=encodeURI(s).replace(P.percentDecode,"%")}catch{return null}return s}function Kt(s,e){var i;const t=s.replace(P.findPipe,(c,l,u)=>{let o=!1,d=l;for(;--d>=0&&u[d]==="\\";)o=!o;return o?"|":" |"}),a=t.split(P.splitPipe);let n=0;if(a[0].trim()||a.shift(),a.length>0&&!((i=a.at(-1))!=null&&i.trim())&&a.pop(),e)if(a.length>e)a.splice(e);else for(;a.length<e;)a.push("");for(;n<a.length;n++)a[n]=a[n].trim().replace(P.slashPipe,"|");return a}function fe(s,e,t){const a=s.length;if(a===0)return"";let n=0;for(;n<a&&s.charAt(a-n-1)===e;)n++;return s.slice(0,a-n)}function ka(s,e){if(s.indexOf(e[1])===-1)return-1;let t=0;for(let a=0;a<s.length;a++)if(s[a]==="\\")a++;else if(s[a]===e[0])t++;else if(s[a]===e[1]&&(t--,t<0))return a;return t>0?-2:-1}function Jt(s,e,t,a,n){const i=e.href,c=e.title||null,l=s[1].replace(n.other.outputLinkReplace,"$1");a.state.inLink=!0;const u={type:s[0].charAt(0)==="!"?"image":"link",raw:t,href:i,title:c,text:l,tokens:a.inlineTokens(l)};return a.state.inLink=!1,u}function Sa(s,e,t){const a=s.match(t.other.indentCodeCompensation);if(a===null)return e;const n=a[1];return e.split(`
`).map(i=>{const c=i.match(t.other.beginningSpace);if(c===null)return i;const[l]=c;return l.length>=n.length?i.slice(n.length):i}).join(`
`)}var Be=class{constructor(s){y(this,"options");y(this,"rules");y(this,"lexer");this.options=s||te}space(s){const e=this.rules.block.newline.exec(s);if(e&&e[0].length>0)return{type:"space",raw:e[0]}}code(s){const e=this.rules.block.code.exec(s);if(e){const t=e[0].replace(this.rules.other.codeRemoveIndent,"");return{type:"code",raw:e[0],codeBlockStyle:"indented",text:this.options.pedantic?t:fe(t,`
`)}}}fences(s){const e=this.rules.block.fences.exec(s);if(e){const t=e[0],a=Sa(t,e[3]||"",this.rules);return{type:"code",raw:t,lang:e[2]?e[2].trim().replace(this.rules.inline.anyPunctuation,"$1"):e[2],text:a}}}heading(s){const e=this.rules.block.heading.exec(s);if(e){let t=e[2].trim();if(this.rules.other.endingHash.test(t)){const a=fe(t,"#");(this.options.pedantic||!a||this.rules.other.endingSpaceChar.test(a))&&(t=a.trim())}return{type:"heading",raw:e[0],depth:e[1].length,text:t,tokens:this.lexer.inline(t)}}}hr(s){const e=this.rules.block.hr.exec(s);if(e)return{type:"hr",raw:fe(e[0],`
`)}}blockquote(s){const e=this.rules.block.blockquote.exec(s);if(e){let t=fe(e[0],`
`).split(`
`),a="",n="";const i=[];for(;t.length>0;){let c=!1;const l=[];let u;for(u=0;u<t.length;u++)if(this.rules.other.blockquoteStart.test(t[u]))l.push(t[u]),c=!0;else if(!c)l.push(t[u]);else break;t=t.slice(u);const o=l.join(`
`),d=o.replace(this.rules.other.blockquoteSetextReplace,`
    $1`).replace(this.rules.other.blockquoteSetextReplace2,"");a=a?`${a}
${o}`:o,n=n?`${n}
${d}`:d;const w=this.lexer.state.top;if(this.lexer.state.top=!0,this.lexer.blockTokens(d,i,!0),this.lexer.state.top=w,t.length===0)break;const h=i.at(-1);if((h==null?void 0:h.type)==="code")break;if((h==null?void 0:h.type)==="blockquote"){const S=h,x=S.raw+`
`+t.join(`
`),I=this.blockquote(x);i[i.length-1]=I,a=a.substring(0,a.length-S.raw.length)+I.raw,n=n.substring(0,n.length-S.text.length)+I.text;break}else if((h==null?void 0:h.type)==="list"){const S=h,x=S.raw+`
`+t.join(`
`),I=this.list(x);i[i.length-1]=I,a=a.substring(0,a.length-h.raw.length)+I.raw,n=n.substring(0,n.length-S.raw.length)+I.raw,t=x.substring(i.at(-1).raw.length).split(`
`);continue}}return{type:"blockquote",raw:a,tokens:i,text:n}}}list(s){let e=this.rules.block.list.exec(s);if(e){let t=e[1].trim();const a=t.length>1,n={type:"list",raw:"",ordered:a,start:a?+t.slice(0,-1):"",loose:!1,items:[]};t=a?`\\d{1,9}\\${t.slice(-1)}`:`\\${t}`,this.options.pedantic&&(t=a?t:"[*+-]");const i=this.rules.other.listItemRegex(t);let c=!1;for(;s;){let u=!1,o="",d="";if(!(e=i.exec(s))||this.rules.block.hr.test(s))break;o=e[0],s=s.substring(o.length);let w=e[2].split(`
`,1)[0].replace(this.rules.other.listReplaceTabs,ce=>" ".repeat(3*ce.length)),h=s.split(`
`,1)[0],S=!w.trim(),x=0;if(this.options.pedantic?(x=2,d=w.trimStart()):S?x=e[1].length+1:(x=e[2].search(this.rules.other.nonSpaceChar),x=x>4?1:x,d=w.slice(x),x+=e[1].length),S&&this.rules.other.blankLine.test(h)&&(o+=h+`
`,s=s.substring(h.length+1),u=!0),!u){const ce=this.rules.other.nextBulletRegex(x),Te=this.rules.other.hrRegex(x),Z=this.rules.other.fencesBeginRegex(x),A=this.rules.other.headingBeginRegex(x),X=this.rules.other.htmlBeginRegex(x);for(;s;){const K=s.split(`
`,1)[0];let J;if(h=K,this.options.pedantic?(h=h.replace(this.rules.other.listReplaceNesting,"  "),J=h):J=h.replace(this.rules.other.tabCharGlobal,"    "),Z.test(h)||A.test(h)||X.test(h)||ce.test(h)||Te.test(h))break;if(J.search(this.rules.other.nonSpaceChar)>=x||!h.trim())d+=`
`+J.slice(x);else{if(S||w.replace(this.rules.other.tabCharGlobal,"    ").search(this.rules.other.nonSpaceChar)>=4||Z.test(w)||A.test(w)||Te.test(w))break;d+=`
`+h}!S&&!h.trim()&&(S=!0),o+=K+`
`,s=s.substring(K.length+1),w=J.slice(x)}}n.loose||(c?n.loose=!0:this.rules.other.doubleBlankLine.test(o)&&(c=!0));let I=null,Se;this.options.gfm&&(I=this.rules.other.listIsTask.exec(d),I&&(Se=I[0]!=="[ ] ",d=d.replace(this.rules.other.listReplaceTask,""))),n.items.push({type:"list_item",raw:o,task:!!I,checked:Se,loose:!1,text:d,tokens:[]}),n.raw+=o}const l=n.items.at(-1);if(l)l.raw=l.raw.trimEnd(),l.text=l.text.trimEnd();else return;n.raw=n.raw.trimEnd();for(let u=0;u<n.items.length;u++)if(this.lexer.state.top=!1,n.items[u].tokens=this.lexer.blockTokens(n.items[u].text,[]),!n.loose){const o=n.items[u].tokens.filter(w=>w.type==="space"),d=o.length>0&&o.some(w=>this.rules.other.anyLine.test(w.raw));n.loose=d}if(n.loose)for(let u=0;u<n.items.length;u++)n.items[u].loose=!0;return n}}html(s){const e=this.rules.block.html.exec(s);if(e)return{type:"html",block:!0,raw:e[0],pre:e[1]==="pre"||e[1]==="script"||e[1]==="style",text:e[0]}}def(s){const e=this.rules.block.def.exec(s);if(e){const t=e[1].toLowerCase().replace(this.rules.other.multipleSpaceGlobal," "),a=e[2]?e[2].replace(this.rules.other.hrefBrackets,"$1").replace(this.rules.inline.anyPunctuation,"$1"):"",n=e[3]?e[3].substring(1,e[3].length-1).replace(this.rules.inline.anyPunctuation,"$1"):e[3];return{type:"def",tag:t,raw:e[0],href:a,title:n}}}table(s){var c;const e=this.rules.block.table.exec(s);if(!e||!this.rules.other.tableDelimiter.test(e[2]))return;const t=Kt(e[1]),a=e[2].replace(this.rules.other.tableAlignChars,"").split("|"),n=(c=e[3])!=null&&c.trim()?e[3].replace(this.rules.other.tableRowBlankLine,"").split(`
`):[],i={type:"table",raw:e[0],header:[],align:[],rows:[]};if(t.length===a.length){for(const l of a)this.rules.other.tableAlignRight.test(l)?i.align.push("right"):this.rules.other.tableAlignCenter.test(l)?i.align.push("center"):this.rules.other.tableAlignLeft.test(l)?i.align.push("left"):i.align.push(null);for(let l=0;l<t.length;l++)i.header.push({text:t[l],tokens:this.lexer.inline(t[l]),header:!0,align:i.align[l]});for(const l of n)i.rows.push(Kt(l,i.header.length).map((u,o)=>({text:u,tokens:this.lexer.inline(u),header:!1,align:i.align[o]})));return i}}lheading(s){const e=this.rules.block.lheading.exec(s);if(e)return{type:"heading",raw:e[0],depth:e[2].charAt(0)==="="?1:2,text:e[1],tokens:this.lexer.inline(e[1])}}paragraph(s){const e=this.rules.block.paragraph.exec(s);if(e){const t=e[1].charAt(e[1].length-1)===`
`?e[1].slice(0,-1):e[1];return{type:"paragraph",raw:e[0],text:t,tokens:this.lexer.inline(t)}}}text(s){const e=this.rules.block.text.exec(s);if(e)return{type:"text",raw:e[0],text:e[0],tokens:this.lexer.inline(e[0])}}escape(s){const e=this.rules.inline.escape.exec(s);if(e)return{type:"escape",raw:e[0],text:e[1]}}tag(s){const e=this.rules.inline.tag.exec(s);if(e)return!this.lexer.state.inLink&&this.rules.other.startATag.test(e[0])?this.lexer.state.inLink=!0:this.lexer.state.inLink&&this.rules.other.endATag.test(e[0])&&(this.lexer.state.inLink=!1),!this.lexer.state.inRawBlock&&this.rules.other.startPreScriptTag.test(e[0])?this.lexer.state.inRawBlock=!0:this.lexer.state.inRawBlock&&this.rules.other.endPreScriptTag.test(e[0])&&(this.lexer.state.inRawBlock=!1),{type:"html",raw:e[0],inLink:this.lexer.state.inLink,inRawBlock:this.lexer.state.inRawBlock,block:!1,text:e[0]}}link(s){const e=this.rules.inline.link.exec(s);if(e){const t=e[2].trim();if(!this.options.pedantic&&this.rules.other.startAngleBracket.test(t)){if(!this.rules.other.endAngleBracket.test(t))return;const i=fe(t.slice(0,-1),"\\");if((t.length-i.length)%2===0)return}else{const i=ka(e[2],"()");if(i===-2)return;if(i>-1){const l=(e[0].indexOf("!")===0?5:4)+e[1].length+i;e[2]=e[2].substring(0,i),e[0]=e[0].substring(0,l).trim(),e[3]=""}}let a=e[2],n="";if(this.options.pedantic){const i=this.rules.other.pedanticHrefTitle.exec(a);i&&(a=i[1],n=i[3])}else n=e[3]?e[3].slice(1,-1):"";return a=a.trim(),this.rules.other.startAngleBracket.test(a)&&(this.options.pedantic&&!this.rules.other.endAngleBracket.test(t)?a=a.slice(1):a=a.slice(1,-1)),Jt(e,{href:a&&a.replace(this.rules.inline.anyPunctuation,"$1"),title:n&&n.replace(this.rules.inline.anyPunctuation,"$1")},e[0],this.lexer,this.rules)}}reflink(s,e){let t;if((t=this.rules.inline.reflink.exec(s))||(t=this.rules.inline.nolink.exec(s))){const a=(t[2]||t[1]).replace(this.rules.other.multipleSpaceGlobal," "),n=e[a.toLowerCase()];if(!n){const i=t[0].charAt(0);return{type:"text",raw:i,text:i}}return Jt(t,n,t[0],this.lexer,this.rules)}}emStrong(s,e,t=""){let a=this.rules.inline.emStrongLDelim.exec(s);if(!a||a[3]&&t.match(this.rules.other.unicodeAlphaNumeric))return;if(!(a[1]||a[2]||"")||!t||this.rules.inline.punctuation.exec(t)){const i=[...a[0]].length-1;let c,l,u=i,o=0;const d=a[0][0]==="*"?this.rules.inline.emStrongRDelimAst:this.rules.inline.emStrongRDelimUnd;for(d.lastIndex=0,e=e.slice(-1*s.length+i);(a=d.exec(e))!=null;){if(c=a[1]||a[2]||a[3]||a[4]||a[5]||a[6],!c)continue;if(l=[...c].length,a[3]||a[4]){u+=l;continue}else if((a[5]||a[6])&&i%3&&!((i+l)%3)){o+=l;continue}if(u-=l,u>0)continue;l=Math.min(l,l+u+o);const w=[...a[0]][0].length,h=s.slice(0,i+a.index+w+l);if(Math.min(i,l)%2){const x=h.slice(1,-1);return{type:"em",raw:h,text:x,tokens:this.lexer.inlineTokens(x)}}const S=h.slice(2,-2);return{type:"strong",raw:h,text:S,tokens:this.lexer.inlineTokens(S)}}}}codespan(s){const e=this.rules.inline.code.exec(s);if(e){let t=e[2].replace(this.rules.other.newLineCharGlobal," ");const a=this.rules.other.nonSpaceChar.test(t),n=this.rules.other.startingSpaceChar.test(t)&&this.rules.other.endingSpaceChar.test(t);return a&&n&&(t=t.substring(1,t.length-1)),{type:"codespan",raw:e[0],text:t}}}br(s){const e=this.rules.inline.br.exec(s);if(e)return{type:"br",raw:e[0]}}del(s){const e=this.rules.inline.del.exec(s);if(e)return{type:"del",raw:e[0],text:e[2],tokens:this.lexer.inlineTokens(e[2])}}autolink(s){const e=this.rules.inline.autolink.exec(s);if(e){let t,a;return e[2]==="@"?(t=e[1],a="mailto:"+t):(t=e[1],a=t),{type:"link",raw:e[0],text:t,href:a,tokens:[{type:"text",raw:t,text:t}]}}}url(s){var t;let e;if(e=this.rules.inline.url.exec(s)){let a,n;if(e[2]==="@")a=e[0],n="mailto:"+a;else{let i;do i=e[0],e[0]=((t=this.rules.inline._backpedal.exec(e[0]))==null?void 0:t[0])??"";while(i!==e[0]);a=e[0],e[1]==="www."?n="http://"+e[0]:n=e[0]}return{type:"link",raw:e[0],text:a,href:n,tokens:[{type:"text",raw:a,text:a}]}}}inlineText(s){const e=this.rules.inline.text.exec(s);if(e){const t=this.lexer.state.inRawBlock;return{type:"text",raw:e[0],text:e[0],escaped:t}}}},V=class ct{constructor(e){y(this,"tokens");y(this,"options");y(this,"state");y(this,"tokenizer");y(this,"inlineQueue");this.tokens=[],this.tokens.links=Object.create(null),this.options=e||te,this.options.tokenizer=this.options.tokenizer||new Be,this.tokenizer=this.options.tokenizer,this.tokenizer.options=this.options,this.tokenizer.lexer=this,this.inlineQueue=[],this.state={inLink:!1,inRawBlock:!1,top:!0};const t={other:P,block:Oe.normal,inline:me.normal};this.options.pedantic?(t.block=Oe.pedantic,t.inline=me.pedantic):this.options.gfm&&(t.block=Oe.gfm,this.options.breaks?t.inline=me.breaks:t.inline=me.gfm),this.tokenizer.rules=t}static get rules(){return{block:Oe,inline:me}}static lex(e,t){return new ct(t).lex(e)}static lexInline(e,t){return new ct(t).inlineTokens(e)}lex(e){e=e.replace(P.carriageReturn,`
`),this.blockTokens(e,this.tokens);for(let t=0;t<this.inlineQueue.length;t++){const a=this.inlineQueue[t];this.inlineTokens(a.src,a.tokens)}return this.inlineQueue=[],this.tokens}blockTokens(e,t=[],a=!1){var n,i,c;for(this.options.pedantic&&(e=e.replace(P.tabCharGlobal,"    ").replace(P.spaceLine,""));e;){let l;if((i=(n=this.options.extensions)==null?void 0:n.block)!=null&&i.some(o=>(l=o.call({lexer:this},e,t))?(e=e.substring(l.raw.length),t.push(l),!0):!1))continue;if(l=this.tokenizer.space(e)){e=e.substring(l.raw.length);const o=t.at(-1);l.raw.length===1&&o!==void 0?o.raw+=`
`:t.push(l);continue}if(l=this.tokenizer.code(e)){e=e.substring(l.raw.length);const o=t.at(-1);(o==null?void 0:o.type)==="paragraph"||(o==null?void 0:o.type)==="text"?(o.raw+=`
`+l.raw,o.text+=`
`+l.text,this.inlineQueue.at(-1).src=o.text):t.push(l);continue}if(l=this.tokenizer.fences(e)){e=e.substring(l.raw.length),t.push(l);continue}if(l=this.tokenizer.heading(e)){e=e.substring(l.raw.length),t.push(l);continue}if(l=this.tokenizer.hr(e)){e=e.substring(l.raw.length),t.push(l);continue}if(l=this.tokenizer.blockquote(e)){e=e.substring(l.raw.length),t.push(l);continue}if(l=this.tokenizer.list(e)){e=e.substring(l.raw.length),t.push(l);continue}if(l=this.tokenizer.html(e)){e=e.substring(l.raw.length),t.push(l);continue}if(l=this.tokenizer.def(e)){e=e.substring(l.raw.length);const o=t.at(-1);(o==null?void 0:o.type)==="paragraph"||(o==null?void 0:o.type)==="text"?(o.raw+=`
`+l.raw,o.text+=`
`+l.raw,this.inlineQueue.at(-1).src=o.text):this.tokens.links[l.tag]||(this.tokens.links[l.tag]={href:l.href,title:l.title});continue}if(l=this.tokenizer.table(e)){e=e.substring(l.raw.length),t.push(l);continue}if(l=this.tokenizer.lheading(e)){e=e.substring(l.raw.length),t.push(l);continue}let u=e;if((c=this.options.extensions)!=null&&c.startBlock){let o=1/0;const d=e.slice(1);let w;this.options.extensions.startBlock.forEach(h=>{w=h.call({lexer:this},d),typeof w=="number"&&w>=0&&(o=Math.min(o,w))}),o<1/0&&o>=0&&(u=e.substring(0,o+1))}if(this.state.top&&(l=this.tokenizer.paragraph(u))){const o=t.at(-1);a&&(o==null?void 0:o.type)==="paragraph"?(o.raw+=`
`+l.raw,o.text+=`
`+l.text,this.inlineQueue.pop(),this.inlineQueue.at(-1).src=o.text):t.push(l),a=u.length!==e.length,e=e.substring(l.raw.length);continue}if(l=this.tokenizer.text(e)){e=e.substring(l.raw.length);const o=t.at(-1);(o==null?void 0:o.type)==="text"?(o.raw+=`
`+l.raw,o.text+=`
`+l.text,this.inlineQueue.pop(),this.inlineQueue.at(-1).src=o.text):t.push(l);continue}if(e){const o="Infinite loop on byte: "+e.charCodeAt(0);if(this.options.silent){console.error(o);break}else throw new Error(o)}}return this.state.top=!0,t}inline(e,t=[]){return this.inlineQueue.push({src:e,tokens:t}),t}inlineTokens(e,t=[]){var l,u,o;let a=e,n=null;if(this.tokens.links){const d=Object.keys(this.tokens.links);if(d.length>0)for(;(n=this.tokenizer.rules.inline.reflinkSearch.exec(a))!=null;)d.includes(n[0].slice(n[0].lastIndexOf("[")+1,-1))&&(a=a.slice(0,n.index)+"["+"a".repeat(n[0].length-2)+"]"+a.slice(this.tokenizer.rules.inline.reflinkSearch.lastIndex))}for(;(n=this.tokenizer.rules.inline.anyPunctuation.exec(a))!=null;)a=a.slice(0,n.index)+"++"+a.slice(this.tokenizer.rules.inline.anyPunctuation.lastIndex);for(;(n=this.tokenizer.rules.inline.blockSkip.exec(a))!=null;)a=a.slice(0,n.index)+"["+"a".repeat(n[0].length-2)+"]"+a.slice(this.tokenizer.rules.inline.blockSkip.lastIndex);let i=!1,c="";for(;e;){i||(c=""),i=!1;let d;if((u=(l=this.options.extensions)==null?void 0:l.inline)!=null&&u.some(h=>(d=h.call({lexer:this},e,t))?(e=e.substring(d.raw.length),t.push(d),!0):!1))continue;if(d=this.tokenizer.escape(e)){e=e.substring(d.raw.length),t.push(d);continue}if(d=this.tokenizer.tag(e)){e=e.substring(d.raw.length),t.push(d);continue}if(d=this.tokenizer.link(e)){e=e.substring(d.raw.length),t.push(d);continue}if(d=this.tokenizer.reflink(e,this.tokens.links)){e=e.substring(d.raw.length);const h=t.at(-1);d.type==="text"&&(h==null?void 0:h.type)==="text"?(h.raw+=d.raw,h.text+=d.text):t.push(d);continue}if(d=this.tokenizer.emStrong(e,a,c)){e=e.substring(d.raw.length),t.push(d);continue}if(d=this.tokenizer.codespan(e)){e=e.substring(d.raw.length),t.push(d);continue}if(d=this.tokenizer.br(e)){e=e.substring(d.raw.length),t.push(d);continue}if(d=this.tokenizer.del(e)){e=e.substring(d.raw.length),t.push(d);continue}if(d=this.tokenizer.autolink(e)){e=e.substring(d.raw.length),t.push(d);continue}if(!this.state.inLink&&(d=this.tokenizer.url(e))){e=e.substring(d.raw.length),t.push(d);continue}let w=e;if((o=this.options.extensions)!=null&&o.startInline){let h=1/0;const S=e.slice(1);let x;this.options.extensions.startInline.forEach(I=>{x=I.call({lexer:this},S),typeof x=="number"&&x>=0&&(h=Math.min(h,x))}),h<1/0&&h>=0&&(w=e.substring(0,h+1))}if(d=this.tokenizer.inlineText(w)){e=e.substring(d.raw.length),d.raw.slice(-1)!=="_"&&(c=d.raw.slice(-1)),i=!0;const h=t.at(-1);(h==null?void 0:h.type)==="text"?(h.raw+=d.raw,h.text+=d.text):t.push(d);continue}if(e){const h="Infinite loop on byte: "+e.charCodeAt(0);if(this.options.silent){console.error(h);break}else throw new Error(h)}}return t}},je=class{constructor(s){y(this,"options");y(this,"parser");this.options=s||te}space(s){return""}code({text:s,lang:e,escaped:t}){var i;const a=(i=(e||"").match(P.notSpaceStart))==null?void 0:i[0],n=s.replace(P.endingNewline,"")+`
`;return a?'<pre><code class="language-'+$(a)+'">'+(t?n:$(n,!0))+`</code></pre>
`:"<pre><code>"+(t?n:$(n,!0))+`</code></pre>
`}blockquote({tokens:s}){return`<blockquote>
${this.parser.parse(s)}</blockquote>
`}html({text:s}){return s}heading({tokens:s,depth:e}){return`<h${e}>${this.parser.parseInline(s)}</h${e}>
`}hr(s){return`<hr>
`}list(s){const e=s.ordered,t=s.start;let a="";for(let c=0;c<s.items.length;c++){const l=s.items[c];a+=this.listitem(l)}const n=e?"ol":"ul",i=e&&t!==1?' start="'+t+'"':"";return"<"+n+i+`>
`+a+"</"+n+`>
`}listitem(s){var t;let e="";if(s.task){const a=this.checkbox({checked:!!s.checked});s.loose?((t=s.tokens[0])==null?void 0:t.type)==="paragraph"?(s.tokens[0].text=a+" "+s.tokens[0].text,s.tokens[0].tokens&&s.tokens[0].tokens.length>0&&s.tokens[0].tokens[0].type==="text"&&(s.tokens[0].tokens[0].text=a+" "+$(s.tokens[0].tokens[0].text),s.tokens[0].tokens[0].escaped=!0)):s.tokens.unshift({type:"text",raw:a+" ",text:a+" ",escaped:!0}):e+=a+" "}return e+=this.parser.parse(s.tokens,!!s.loose),`<li>${e}</li>
`}checkbox({checked:s}){return"<input "+(s?'checked="" ':"")+'disabled="" type="checkbox">'}paragraph({tokens:s}){return`<p>${this.parser.parseInline(s)}</p>
`}table(s){let e="",t="";for(let n=0;n<s.header.length;n++)t+=this.tablecell(s.header[n]);e+=this.tablerow({text:t});let a="";for(let n=0;n<s.rows.length;n++){const i=s.rows[n];t="";for(let c=0;c<i.length;c++)t+=this.tablecell(i[c]);a+=this.tablerow({text:t})}return a&&(a=`<tbody>${a}</tbody>`),`<table>
<thead>
`+e+`</thead>
`+a+`</table>
`}tablerow({text:s}){return`<tr>
${s}</tr>
`}tablecell(s){const e=this.parser.parseInline(s.tokens),t=s.header?"th":"td";return(s.align?`<${t} align="${s.align}">`:`<${t}>`)+e+`</${t}>
`}strong({tokens:s}){return`<strong>${this.parser.parseInline(s)}</strong>`}em({tokens:s}){return`<em>${this.parser.parseInline(s)}</em>`}codespan({text:s}){return`<code>${$(s,!0)}</code>`}br(s){return"<br>"}del({tokens:s}){return`<del>${this.parser.parseInline(s)}</del>`}link({href:s,title:e,tokens:t}){const a=this.parser.parseInline(t),n=Xt(s);if(n===null)return a;s=n;let i='<a href="'+s+'"';return e&&(i+=' title="'+$(e)+'"'),i+=">"+a+"</a>",i}image({href:s,title:e,text:t,tokens:a}){a&&(t=this.parser.parseInline(a,this.parser.textRenderer));const n=Xt(s);if(n===null)return $(t);s=n;let i=`<img src="${s}" alt="${t}"`;return e&&(i+=` title="${$(e)}"`),i+=">",i}text(s){return"tokens"in s&&s.tokens?this.parser.parseInline(s.tokens):"escaped"in s&&s.escaped?s.text:$(s.text)}},yt=class{strong({text:s}){return s}em({text:s}){return s}codespan({text:s}){return s}del({text:s}){return s}html({text:s}){return s}text({text:s}){return s}link({text:s}){return""+s}image({text:s}){return""+s}br(){return""}},Y=class dt{constructor(e){y(this,"options");y(this,"renderer");y(this,"textRenderer");this.options=e||te,this.options.renderer=this.options.renderer||new je,this.renderer=this.options.renderer,this.renderer.options=this.options,this.renderer.parser=this,this.textRenderer=new yt}static parse(e,t){return new dt(t).parse(e)}static parseInline(e,t){return new dt(t).parseInline(e)}parse(e,t=!0){var n,i;let a="";for(let c=0;c<e.length;c++){const l=e[c];if((i=(n=this.options.extensions)==null?void 0:n.renderers)!=null&&i[l.type]){const o=l,d=this.options.extensions.renderers[o.type].call({parser:this},o);if(d!==!1||!["space","hr","heading","code","table","blockquote","list","html","paragraph","text"].includes(o.type)){a+=d||"";continue}}const u=l;switch(u.type){case"space":{a+=this.renderer.space(u);continue}case"hr":{a+=this.renderer.hr(u);continue}case"heading":{a+=this.renderer.heading(u);continue}case"code":{a+=this.renderer.code(u);continue}case"table":{a+=this.renderer.table(u);continue}case"blockquote":{a+=this.renderer.blockquote(u);continue}case"list":{a+=this.renderer.list(u);continue}case"html":{a+=this.renderer.html(u);continue}case"paragraph":{a+=this.renderer.paragraph(u);continue}case"text":{let o=u,d=this.renderer.text(o);for(;c+1<e.length&&e[c+1].type==="text";)o=e[++c],d+=`
`+this.renderer.text(o);t?a+=this.renderer.paragraph({type:"paragraph",raw:d,text:d,tokens:[{type:"text",raw:d,text:d,escaped:!0}]}):a+=d;continue}default:{const o='Token with "'+u.type+'" type was not found.';if(this.options.silent)return console.error(o),"";throw new Error(o)}}}return a}parseInline(e,t=this.renderer){var n,i;let a="";for(let c=0;c<e.length;c++){const l=e[c];if((i=(n=this.options.extensions)==null?void 0:n.renderers)!=null&&i[l.type]){const o=this.options.extensions.renderers[l.type].call({parser:this},l);if(o!==!1||!["escape","html","link","image","strong","em","codespan","br","del","text"].includes(l.type)){a+=o||"";continue}}const u=l;switch(u.type){case"escape":{a+=t.text(u);break}case"html":{a+=t.html(u);break}case"link":{a+=t.link(u);break}case"image":{a+=t.image(u);break}case"strong":{a+=t.strong(u);break}case"em":{a+=t.em(u);break}case"codespan":{a+=t.codespan(u);break}case"br":{a+=t.br(u);break}case"del":{a+=t.del(u);break}case"text":{a+=t.text(u);break}default:{const o='Token with "'+u.type+'" type was not found.';if(this.options.silent)return console.error(o),"";throw new Error(o)}}}return a}},lt,Pe=(lt=class{constructor(s){y(this,"options");y(this,"block");this.options=s||te}preprocess(s){return s}postprocess(s){return s}processAllTokens(s){return s}provideLexer(){return this.block?V.lex:V.lexInline}provideParser(){return this.block?Y.parse:Y.parseInline}},y(lt,"passThroughHooks",new Set(["preprocess","postprocess","processAllTokens"])),lt),Ta=class{constructor(...s){y(this,"defaults",ht());y(this,"options",this.setOptions);y(this,"parse",this.parseMarkdown(!0));y(this,"parseInline",this.parseMarkdown(!1));y(this,"Parser",Y);y(this,"Renderer",je);y(this,"TextRenderer",yt);y(this,"Lexer",V);y(this,"Tokenizer",Be);y(this,"Hooks",Pe);this.use(...s)}walkTokens(s,e){var a,n;let t=[];for(const i of s)switch(t=t.concat(e.call(this,i)),i.type){case"table":{const c=i;for(const l of c.header)t=t.concat(this.walkTokens(l.tokens,e));for(const l of c.rows)for(const u of l)t=t.concat(this.walkTokens(u.tokens,e));break}case"list":{const c=i;t=t.concat(this.walkTokens(c.items,e));break}default:{const c=i;(n=(a=this.defaults.extensions)==null?void 0:a.childTokens)!=null&&n[c.type]?this.defaults.extensions.childTokens[c.type].forEach(l=>{const u=c[l].flat(1/0);t=t.concat(this.walkTokens(u,e))}):c.tokens&&(t=t.concat(this.walkTokens(c.tokens,e)))}}return t}use(...s){const e=this.defaults.extensions||{renderers:{},childTokens:{}};return s.forEach(t=>{const a={...t};if(a.async=this.defaults.async||a.async||!1,t.extensions&&(t.extensions.forEach(n=>{if(!n.name)throw new Error("extension name required");if("renderer"in n){const i=e.renderers[n.name];i?e.renderers[n.name]=function(...c){let l=n.renderer.apply(this,c);return l===!1&&(l=i.apply(this,c)),l}:e.renderers[n.name]=n.renderer}if("tokenizer"in n){if(!n.level||n.level!=="block"&&n.level!=="inline")throw new Error("extension level must be 'block' or 'inline'");const i=e[n.level];i?i.unshift(n.tokenizer):e[n.level]=[n.tokenizer],n.start&&(n.level==="block"?e.startBlock?e.startBlock.push(n.start):e.startBlock=[n.start]:n.level==="inline"&&(e.startInline?e.startInline.push(n.start):e.startInline=[n.start]))}"childTokens"in n&&n.childTokens&&(e.childTokens[n.name]=n.childTokens)}),a.extensions=e),t.renderer){const n=this.defaults.renderer||new je(this.defaults);for(const i in t.renderer){if(!(i in n))throw new Error(`renderer '${i}' does not exist`);if(["options","parser"].includes(i))continue;const c=i,l=t.renderer[c],u=n[c];n[c]=(...o)=>{let d=l.apply(n,o);return d===!1&&(d=u.apply(n,o)),d||""}}a.renderer=n}if(t.tokenizer){const n=this.defaults.tokenizer||new Be(this.defaults);for(const i in t.tokenizer){if(!(i in n))throw new Error(`tokenizer '${i}' does not exist`);if(["options","rules","lexer"].includes(i))continue;const c=i,l=t.tokenizer[c],u=n[c];n[c]=(...o)=>{let d=l.apply(n,o);return d===!1&&(d=u.apply(n,o)),d}}a.tokenizer=n}if(t.hooks){const n=this.defaults.hooks||new Pe;for(const i in t.hooks){if(!(i in n))throw new Error(`hook '${i}' does not exist`);if(["options","block"].includes(i))continue;const c=i,l=t.hooks[c],u=n[c];Pe.passThroughHooks.has(i)?n[c]=o=>{if(this.defaults.async)return Promise.resolve(l.call(n,o)).then(w=>u.call(n,w));const d=l.call(n,o);return u.call(n,d)}:n[c]=(...o)=>{let d=l.apply(n,o);return d===!1&&(d=u.apply(n,o)),d}}a.hooks=n}if(t.walkTokens){const n=this.defaults.walkTokens,i=t.walkTokens;a.walkTokens=function(c){let l=[];return l.push(i.call(this,c)),n&&(l=l.concat(n.call(this,c))),l}}this.defaults={...this.defaults,...a}}),this}setOptions(s){return this.defaults={...this.defaults,...s},this}lexer(s,e){return V.lex(s,e??this.defaults)}parser(s,e){return Y.parse(s,e??this.defaults)}parseMarkdown(s){return(t,a)=>{const n={...a},i={...this.defaults,...n},c=this.onError(!!i.silent,!!i.async);if(this.defaults.async===!0&&n.async===!1)return c(new Error("marked(): The async option was set to true by an extension. Remove async: false from the parse options object to return a Promise."));if(typeof t>"u"||t===null)return c(new Error("marked(): input parameter is undefined or null"));if(typeof t!="string")return c(new Error("marked(): input parameter is of type "+Object.prototype.toString.call(t)+", string expected"));i.hooks&&(i.hooks.options=i,i.hooks.block=s);const l=i.hooks?i.hooks.provideLexer():s?V.lex:V.lexInline,u=i.hooks?i.hooks.provideParser():s?Y.parse:Y.parseInline;if(i.async)return Promise.resolve(i.hooks?i.hooks.preprocess(t):t).then(o=>l(o,i)).then(o=>i.hooks?i.hooks.processAllTokens(o):o).then(o=>i.walkTokens?Promise.all(this.walkTokens(o,i.walkTokens)).then(()=>o):o).then(o=>u(o,i)).then(o=>i.hooks?i.hooks.postprocess(o):o).catch(c);try{i.hooks&&(t=i.hooks.preprocess(t));let o=l(t,i);i.hooks&&(o=i.hooks.processAllTokens(o)),i.walkTokens&&this.walkTokens(o,i.walkTokens);let d=u(o,i);return i.hooks&&(d=i.hooks.postprocess(d)),d}catch(o){return c(o)}}}onError(s,e){return t=>{if(t.message+=`
Please report this to https://github.com/markedjs/marked.`,s){const a="<p>An error occurred:</p><pre>"+$(t.message+"",!0)+"</pre>";return e?Promise.resolve(a):a}if(e)return Promise.reject(t);throw t}}},ee=new Ta;function v(s,e){return ee.parse(s,e)}v.options=v.setOptions=function(s){return ee.setOptions(s),v.defaults=ee.defaults,os(v.defaults),v};v.getDefaults=ht;v.defaults=te;v.use=function(...s){return ee.use(...s),v.defaults=ee.defaults,os(v.defaults),v};v.walkTokens=function(s,e){return ee.walkTokens(s,e)};v.parseInline=ee.parseInline;v.Parser=Y;v.parser=Y.parse;v.Renderer=je;v.TextRenderer=yt;v.Lexer=V;v.lexer=V.lex;v.Tokenizer=Be;v.Hooks=Pe;v.parse=v;v.options;v.setOptions;v.use;v.walkTokens;v.parseInline;Y.parse;V.lex;/*! @license DOMPurify 3.2.6 | (c) Cure53 and other contributors | Released under the Apache license 2.0 and Mozilla Public License 2.0 | github.com/cure53/DOMPurify/blob/3.2.6/LICENSE */const{entries:vs,setPrototypeOf:Qt,isFrozen:Ea,getPrototypeOf:Aa,getOwnPropertyDescriptor:_a}=Object;let{freeze:D,seal:j,create:ws}=Object,{apply:pt,construct:ut}=typeof Reflect<"u"&&Reflect;D||(D=function(e){return e});j||(j=function(e){return e});pt||(pt=function(e,t,a){return e.apply(t,a)});ut||(ut=function(e,t){return new e(...t)});const Ne=z(Array.prototype.forEach),Ra=z(Array.prototype.lastIndexOf),es=z(Array.prototype.pop),ge=z(Array.prototype.push),La=z(Array.prototype.splice),De=z(String.prototype.toLowerCase),st=z(String.prototype.toString),ts=z(String.prototype.match),xe=z(String.prototype.replace),Ia=z(String.prototype.indexOf),Ca=z(String.prototype.trim),H=z(Object.prototype.hasOwnProperty),M=z(RegExp.prototype.test),be=Oa(TypeError);function z(s){return function(e){e instanceof RegExp&&(e.lastIndex=0);for(var t=arguments.length,a=new Array(t>1?t-1:0),n=1;n<t;n++)a[n-1]=arguments[n];return pt(s,e,a)}}function Oa(s){return function(){for(var e=arguments.length,t=new Array(e),a=0;a<e;a++)t[a]=arguments[a];return ut(s,t)}}function g(s,e){let t=arguments.length>2&&arguments[2]!==void 0?arguments[2]:De;Qt&&Qt(s,null);let a=e.length;for(;a--;){let n=e[a];if(typeof n=="string"){const i=t(n);i!==n&&(Ea(e)||(e[a]=i),n=i)}s[n]=!0}return s}function Na(s){for(let e=0;e<s.length;e++)H(s,e)||(s[e]=null);return s}function W(s){const e=ws(null);for(const[t,a]of vs(s))H(s,t)&&(Array.isArray(a)?e[t]=Na(a):a&&typeof a=="object"&&a.constructor===Object?e[t]=W(a):e[t]=a);return e}function ve(s,e){for(;s!==null;){const a=_a(s,e);if(a){if(a.get)return z(a.get);if(typeof a.value=="function")return z(a.value)}s=Aa(s)}function t(){return null}return t}const ss=D(["a","abbr","acronym","address","area","article","aside","audio","b","bdi","bdo","big","blink","blockquote","body","br","button","canvas","caption","center","cite","code","col","colgroup","content","data","datalist","dd","decorator","del","details","dfn","dialog","dir","div","dl","dt","element","em","fieldset","figcaption","figure","font","footer","form","h1","h2","h3","h4","h5","h6","head","header","hgroup","hr","html","i","img","input","ins","kbd","label","legend","li","main","map","mark","marquee","menu","menuitem","meter","nav","nobr","ol","optgroup","option","output","p","picture","pre","progress","q","rp","rt","ruby","s","samp","section","select","shadow","small","source","spacer","span","strike","strong","style","sub","summary","sup","table","tbody","td","template","textarea","tfoot","th","thead","time","tr","track","tt","u","ul","var","video","wbr"]),at=D(["svg","a","altglyph","altglyphdef","altglyphitem","animatecolor","animatemotion","animatetransform","circle","clippath","defs","desc","ellipse","filter","font","g","glyph","glyphref","hkern","image","line","lineargradient","marker","mask","metadata","mpath","path","pattern","polygon","polyline","radialgradient","rect","stop","style","switch","symbol","text","textpath","title","tref","tspan","view","vkern"]),nt=D(["feBlend","feColorMatrix","feComponentTransfer","feComposite","feConvolveMatrix","feDiffuseLighting","feDisplacementMap","feDistantLight","feDropShadow","feFlood","feFuncA","feFuncB","feFuncG","feFuncR","feGaussianBlur","feImage","feMerge","feMergeNode","feMorphology","feOffset","fePointLight","feSpecularLighting","feSpotLight","feTile","feTurbulence"]),Ma=D(["animate","color-profile","cursor","discard","font-face","font-face-format","font-face-name","font-face-src","font-face-uri","foreignobject","hatch","hatchpath","mesh","meshgradient","meshpatch","meshrow","missing-glyph","script","set","solidcolor","unknown","use"]),it=D(["math","menclose","merror","mfenced","mfrac","mglyph","mi","mlabeledtr","mmultiscripts","mn","mo","mover","mpadded","mphantom","mroot","mrow","ms","mspace","msqrt","mstyle","msub","msup","msubsup","mtable","mtd","mtext","mtr","munder","munderover","mprescripts"]),Pa=D(["maction","maligngroup","malignmark","mlongdiv","mscarries","mscarry","msgroup","mstack","msline","msrow","semantics","annotation","annotation-xml","mprescripts","none"]),as=D(["#text"]),ns=D(["accept","action","align","alt","autocapitalize","autocomplete","autopictureinpicture","autoplay","background","bgcolor","border","capture","cellpadding","cellspacing","checked","cite","class","clear","color","cols","colspan","controls","controlslist","coords","crossorigin","datetime","decoding","default","dir","disabled","disablepictureinpicture","disableremoteplayback","download","draggable","enctype","enterkeyhint","face","for","headers","height","hidden","high","href","hreflang","id","inputmode","integrity","ismap","kind","label","lang","list","loading","loop","low","max","maxlength","media","method","min","minlength","multiple","muted","name","nonce","noshade","novalidate","nowrap","open","optimum","pattern","placeholder","playsinline","popover","popovertarget","popovertargetaction","poster","preload","pubdate","radiogroup","readonly","rel","required","rev","reversed","role","rows","rowspan","spellcheck","scope","selected","shape","size","sizes","span","srclang","start","src","srcset","step","style","summary","tabindex","title","translate","type","usemap","valign","value","width","wrap","xmlns","slot"]),rt=D(["accent-height","accumulate","additive","alignment-baseline","amplitude","ascent","attributename","attributetype","azimuth","basefrequency","baseline-shift","begin","bias","by","class","clip","clippathunits","clip-path","clip-rule","color","color-interpolation","color-interpolation-filters","color-profile","color-rendering","cx","cy","d","dx","dy","diffuseconstant","direction","display","divisor","dur","edgemode","elevation","end","exponent","fill","fill-opacity","fill-rule","filter","filterunits","flood-color","flood-opacity","font-family","font-size","font-size-adjust","font-stretch","font-style","font-variant","font-weight","fx","fy","g1","g2","glyph-name","glyphref","gradientunits","gradienttransform","height","href","id","image-rendering","in","in2","intercept","k","k1","k2","k3","k4","kerning","keypoints","keysplines","keytimes","lang","lengthadjust","letter-spacing","kernelmatrix","kernelunitlength","lighting-color","local","marker-end","marker-mid","marker-start","markerheight","markerunits","markerwidth","maskcontentunits","maskunits","max","mask","media","method","mode","min","name","numoctaves","offset","operator","opacity","order","orient","orientation","origin","overflow","paint-order","path","pathlength","patterncontentunits","patterntransform","patternunits","points","preservealpha","preserveaspectratio","primitiveunits","r","rx","ry","radius","refx","refy","repeatcount","repeatdur","restart","result","rotate","scale","seed","shape-rendering","slope","specularconstant","specularexponent","spreadmethod","startoffset","stddeviation","stitchtiles","stop-color","stop-opacity","stroke-dasharray","stroke-dashoffset","stroke-linecap","stroke-linejoin","stroke-miterlimit","stroke-opacity","stroke","stroke-width","style","surfacescale","systemlanguage","tabindex","tablevalues","targetx","targety","transform","transform-origin","text-anchor","text-decoration","text-rendering","textlength","type","u1","u2","unicode","values","viewbox","visibility","version","vert-adv-y","vert-origin-x","vert-origin-y","width","word-spacing","wrap","writing-mode","xchannelselector","ychannelselector","x","x1","x2","xmlns","y","y1","y2","z","zoomandpan"]),is=D(["accent","accentunder","align","bevelled","close","columnsalign","columnlines","columnspan","denomalign","depth","dir","display","displaystyle","encoding","fence","frame","height","href","id","largeop","length","linethickness","lspace","lquote","mathbackground","mathcolor","mathsize","mathvariant","maxsize","minsize","movablelimits","notation","numalign","open","rowalign","rowlines","rowspacing","rowspan","rspace","rquote","scriptlevel","scriptminsize","scriptsizemultiplier","selection","separator","separators","stretchy","subscriptshift","supscriptshift","symmetric","voffset","width","xmlns"]),Me=D(["xlink:href","xml:id","xlink:title","xml:space","xmlns:xlink"]),Da=j(/\{\{[\w\W]*|[\w\W]*\}\}/gm),za=j(/<%[\w\W]*|[\w\W]*%>/gm),Ba=j(/\$\{[\w\W]*/gm),ja=j(/^data-[\-\w.\u00B7-\uFFFF]+$/),Ha=j(/^aria-[\-\w]+$/),ys=j(/^(?:(?:(?:f|ht)tps?|mailto|tel|callto|sms|cid|xmpp|matrix):|[^a-z]|[a-z+.\-]+(?:[^a-z+.\-:]|$))/i),Fa=j(/^(?:\w+script|data):/i),$a=j(/[\u0000-\u0020\u00A0\u1680\u180E\u2000-\u2029\u205F\u3000]/g),ks=j(/^html$/i),Ua=j(/^[a-z][.\w]*(-[.\w]+)+$/i);var rs=Object.freeze({__proto__:null,ARIA_ATTR:Ha,ATTR_WHITESPACE:$a,CUSTOM_ELEMENT:Ua,DATA_ATTR:ja,DOCTYPE_NAME:ks,ERB_EXPR:za,IS_ALLOWED_URI:ys,IS_SCRIPT_OR_DATA:Fa,MUSTACHE_EXPR:Da,TMPLIT_EXPR:Ba});const we={element:1,text:3,progressingInstruction:7,comment:8,document:9},Ga=function(){return typeof window>"u"?null:window},qa=function(e,t){if(typeof e!="object"||typeof e.createPolicy!="function")return null;let a=null;const n="data-tt-policy-suffix";t&&t.hasAttribute(n)&&(a=t.getAttribute(n));const i="dompurify"+(a?"#"+a:"");try{return e.createPolicy(i,{createHTML(c){return c},createScriptURL(c){return c}})}catch{return console.warn("TrustedTypes policy "+i+" could not be created."),null}},ls=function(){return{afterSanitizeAttributes:[],afterSanitizeElements:[],afterSanitizeShadowDOM:[],beforeSanitizeAttributes:[],beforeSanitizeElements:[],beforeSanitizeShadowDOM:[],uponSanitizeAttribute:[],uponSanitizeElement:[],uponSanitizeShadowNode:[]}};function Ss(){let s=arguments.length>0&&arguments[0]!==void 0?arguments[0]:Ga();const e=f=>Ss(f);if(e.version="3.2.6",e.removed=[],!s||!s.document||s.document.nodeType!==we.document||!s.Element)return e.isSupported=!1,e;let{document:t}=s;const a=t,n=a.currentScript,{DocumentFragment:i,HTMLTemplateElement:c,Node:l,Element:u,NodeFilter:o,NamedNodeMap:d=s.NamedNodeMap||s.MozNamedAttrMap,HTMLFormElement:w,DOMParser:h,trustedTypes:S}=s,x=u.prototype,I=ve(x,"cloneNode"),Se=ve(x,"remove"),ce=ve(x,"nextSibling"),Te=ve(x,"childNodes"),Z=ve(x,"parentNode");if(typeof c=="function"){const f=t.createElement("template");f.content&&f.content.ownerDocument&&(t=f.content.ownerDocument)}let A,X="";const{implementation:K,createNodeIterator:J,createDocumentFragment:Ts,getElementsByTagName:Es}=t,{importNode:As}=a;let N=ls();e.isSupported=typeof vs=="function"&&typeof Z=="function"&&K&&K.createHTMLDocument!==void 0;const{MUSTACHE_EXPR:$e,ERB_EXPR:Ue,TMPLIT_EXPR:Ge,DATA_ATTR:_s,ARIA_ATTR:Rs,IS_SCRIPT_OR_DATA:Ls,ATTR_WHITESPACE:kt,CUSTOM_ELEMENT:Is}=rs;let{IS_ALLOWED_URI:St}=rs,_=null;const Tt=g({},[...ss,...at,...nt,...it,...as]);let L=null;const Et=g({},[...ns,...rt,...is,...Me]);let T=Object.seal(ws(null,{tagNameCheck:{writable:!0,configurable:!1,enumerable:!0,value:null},attributeNameCheck:{writable:!0,configurable:!1,enumerable:!0,value:null},allowCustomizedBuiltInElements:{writable:!0,configurable:!1,enumerable:!0,value:!1}})),de=null,qe=null,At=!0,We=!0,_t=!1,Rt=!0,se=!1,Ee=!0,Q=!1,Ve=!1,Ye=!1,ae=!1,Ae=!1,_e=!1,Lt=!0,It=!1;const Cs="user-content-";let Ze=!0,pe=!1,ne={},ie=null;const Ct=g({},["annotation-xml","audio","colgroup","desc","foreignobject","head","iframe","math","mi","mn","mo","ms","mtext","noembed","noframes","noscript","plaintext","script","style","svg","template","thead","title","video","xmp"]);let Ot=null;const Nt=g({},["audio","video","img","source","image","track"]);let Xe=null;const Mt=g({},["alt","class","for","id","label","name","pattern","placeholder","role","summary","title","value","style","xmlns"]),Re="http://www.w3.org/1998/Math/MathML",Le="http://www.w3.org/2000/svg",U="http://www.w3.org/1999/xhtml";let re=U,Ke=!1,Je=null;const Os=g({},[Re,Le,U],st);let Ie=g({},["mi","mo","mn","ms","mtext"]),Ce=g({},["annotation-xml"]);const Ns=g({},["title","style","font","a","script"]);let ue=null;const Ms=["application/xhtml+xml","text/html"],Ps="text/html";let R=null,le=null;const Ds=t.createElement("form"),Pt=function(r){return r instanceof RegExp||r instanceof Function},Qe=function(){let r=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{};if(!(le&&le===r)){if((!r||typeof r!="object")&&(r={}),r=W(r),ue=Ms.indexOf(r.PARSER_MEDIA_TYPE)===-1?Ps:r.PARSER_MEDIA_TYPE,R=ue==="application/xhtml+xml"?st:De,_=H(r,"ALLOWED_TAGS")?g({},r.ALLOWED_TAGS,R):Tt,L=H(r,"ALLOWED_ATTR")?g({},r.ALLOWED_ATTR,R):Et,Je=H(r,"ALLOWED_NAMESPACES")?g({},r.ALLOWED_NAMESPACES,st):Os,Xe=H(r,"ADD_URI_SAFE_ATTR")?g(W(Mt),r.ADD_URI_SAFE_ATTR,R):Mt,Ot=H(r,"ADD_DATA_URI_TAGS")?g(W(Nt),r.ADD_DATA_URI_TAGS,R):Nt,ie=H(r,"FORBID_CONTENTS")?g({},r.FORBID_CONTENTS,R):Ct,de=H(r,"FORBID_TAGS")?g({},r.FORBID_TAGS,R):W({}),qe=H(r,"FORBID_ATTR")?g({},r.FORBID_ATTR,R):W({}),ne=H(r,"USE_PROFILES")?r.USE_PROFILES:!1,At=r.ALLOW_ARIA_ATTR!==!1,We=r.ALLOW_DATA_ATTR!==!1,_t=r.ALLOW_UNKNOWN_PROTOCOLS||!1,Rt=r.ALLOW_SELF_CLOSE_IN_ATTR!==!1,se=r.SAFE_FOR_TEMPLATES||!1,Ee=r.SAFE_FOR_XML!==!1,Q=r.WHOLE_DOCUMENT||!1,ae=r.RETURN_DOM||!1,Ae=r.RETURN_DOM_FRAGMENT||!1,_e=r.RETURN_TRUSTED_TYPE||!1,Ye=r.FORCE_BODY||!1,Lt=r.SANITIZE_DOM!==!1,It=r.SANITIZE_NAMED_PROPS||!1,Ze=r.KEEP_CONTENT!==!1,pe=r.IN_PLACE||!1,St=r.ALLOWED_URI_REGEXP||ys,re=r.NAMESPACE||U,Ie=r.MATHML_TEXT_INTEGRATION_POINTS||Ie,Ce=r.HTML_INTEGRATION_POINTS||Ce,T=r.CUSTOM_ELEMENT_HANDLING||{},r.CUSTOM_ELEMENT_HANDLING&&Pt(r.CUSTOM_ELEMENT_HANDLING.tagNameCheck)&&(T.tagNameCheck=r.CUSTOM_ELEMENT_HANDLING.tagNameCheck),r.CUSTOM_ELEMENT_HANDLING&&Pt(r.CUSTOM_ELEMENT_HANDLING.attributeNameCheck)&&(T.attributeNameCheck=r.CUSTOM_ELEMENT_HANDLING.attributeNameCheck),r.CUSTOM_ELEMENT_HANDLING&&typeof r.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements=="boolean"&&(T.allowCustomizedBuiltInElements=r.CUSTOM_ELEMENT_HANDLING.allowCustomizedBuiltInElements),se&&(We=!1),Ae&&(ae=!0),ne&&(_=g({},as),L=[],ne.html===!0&&(g(_,ss),g(L,ns)),ne.svg===!0&&(g(_,at),g(L,rt),g(L,Me)),ne.svgFilters===!0&&(g(_,nt),g(L,rt),g(L,Me)),ne.mathMl===!0&&(g(_,it),g(L,is),g(L,Me))),r.ADD_TAGS&&(_===Tt&&(_=W(_)),g(_,r.ADD_TAGS,R)),r.ADD_ATTR&&(L===Et&&(L=W(L)),g(L,r.ADD_ATTR,R)),r.ADD_URI_SAFE_ATTR&&g(Xe,r.ADD_URI_SAFE_ATTR,R),r.FORBID_CONTENTS&&(ie===Ct&&(ie=W(ie)),g(ie,r.FORBID_CONTENTS,R)),Ze&&(_["#text"]=!0),Q&&g(_,["html","head","body"]),_.table&&(g(_,["tbody"]),delete de.tbody),r.TRUSTED_TYPES_POLICY){if(typeof r.TRUSTED_TYPES_POLICY.createHTML!="function")throw be('TRUSTED_TYPES_POLICY configuration option must provide a "createHTML" hook.');if(typeof r.TRUSTED_TYPES_POLICY.createScriptURL!="function")throw be('TRUSTED_TYPES_POLICY configuration option must provide a "createScriptURL" hook.');A=r.TRUSTED_TYPES_POLICY,X=A.createHTML("")}else A===void 0&&(A=qa(S,n)),A!==null&&typeof X=="string"&&(X=A.createHTML(""));D&&D(r),le=r}},Dt=g({},[...at,...nt,...Ma]),zt=g({},[...it,...Pa]),zs=function(r){let p=Z(r);(!p||!p.tagName)&&(p={namespaceURI:re,tagName:"template"});const m=De(r.tagName),k=De(p.tagName);return Je[r.namespaceURI]?r.namespaceURI===Le?p.namespaceURI===U?m==="svg":p.namespaceURI===Re?m==="svg"&&(k==="annotation-xml"||Ie[k]):!!Dt[m]:r.namespaceURI===Re?p.namespaceURI===U?m==="math":p.namespaceURI===Le?m==="math"&&Ce[k]:!!zt[m]:r.namespaceURI===U?p.namespaceURI===Le&&!Ce[k]||p.namespaceURI===Re&&!Ie[k]?!1:!zt[m]&&(Ns[m]||!Dt[m]):!!(ue==="application/xhtml+xml"&&Je[r.namespaceURI]):!1},F=function(r){ge(e.removed,{element:r});try{Z(r).removeChild(r)}catch{Se(r)}},oe=function(r,p){try{ge(e.removed,{attribute:p.getAttributeNode(r),from:p})}catch{ge(e.removed,{attribute:null,from:p})}if(p.removeAttribute(r),r==="is")if(ae||Ae)try{F(p)}catch{}else try{p.setAttribute(r,"")}catch{}},Bt=function(r){let p=null,m=null;if(Ye)r="<remove></remove>"+r;else{const E=ts(r,/^[\r\n\t ]+/);m=E&&E[0]}ue==="application/xhtml+xml"&&re===U&&(r='<html xmlns="http://www.w3.org/1999/xhtml"><head></head><body>'+r+"</body></html>");const k=A?A.createHTML(r):r;if(re===U)try{p=new h().parseFromString(k,ue)}catch{}if(!p||!p.documentElement){p=K.createDocument(re,"template",null);try{p.documentElement.innerHTML=Ke?X:k}catch{}}const C=p.body||p.documentElement;return r&&m&&C.insertBefore(t.createTextNode(m),C.childNodes[0]||null),re===U?Es.call(p,Q?"html":"body")[0]:Q?p.documentElement:C},jt=function(r){return J.call(r.ownerDocument||r,r,o.SHOW_ELEMENT|o.SHOW_COMMENT|o.SHOW_TEXT|o.SHOW_PROCESSING_INSTRUCTION|o.SHOW_CDATA_SECTION,null)},et=function(r){return r instanceof w&&(typeof r.nodeName!="string"||typeof r.textContent!="string"||typeof r.removeChild!="function"||!(r.attributes instanceof d)||typeof r.removeAttribute!="function"||typeof r.setAttribute!="function"||typeof r.namespaceURI!="string"||typeof r.insertBefore!="function"||typeof r.hasChildNodes!="function")},Ht=function(r){return typeof l=="function"&&r instanceof l};function G(f,r,p){Ne(f,m=>{m.call(e,r,p,le)})}const Ft=function(r){let p=null;if(G(N.beforeSanitizeElements,r,null),et(r))return F(r),!0;const m=R(r.nodeName);if(G(N.uponSanitizeElement,r,{tagName:m,allowedTags:_}),Ee&&r.hasChildNodes()&&!Ht(r.firstElementChild)&&M(/<[/\w!]/g,r.innerHTML)&&M(/<[/\w!]/g,r.textContent)||r.nodeType===we.progressingInstruction||Ee&&r.nodeType===we.comment&&M(/<[/\w]/g,r.data))return F(r),!0;if(!_[m]||de[m]){if(!de[m]&&Ut(m)&&(T.tagNameCheck instanceof RegExp&&M(T.tagNameCheck,m)||T.tagNameCheck instanceof Function&&T.tagNameCheck(m)))return!1;if(Ze&&!ie[m]){const k=Z(r)||r.parentNode,C=Te(r)||r.childNodes;if(C&&k){const E=C.length;for(let B=E-1;B>=0;--B){const q=I(C[B],!0);q.__removalCount=(r.__removalCount||0)+1,k.insertBefore(q,ce(r))}}}return F(r),!0}return r instanceof u&&!zs(r)||(m==="noscript"||m==="noembed"||m==="noframes")&&M(/<\/no(script|embed|frames)/i,r.innerHTML)?(F(r),!0):(se&&r.nodeType===we.text&&(p=r.textContent,Ne([$e,Ue,Ge],k=>{p=xe(p,k," ")}),r.textContent!==p&&(ge(e.removed,{element:r.cloneNode()}),r.textContent=p)),G(N.afterSanitizeElements,r,null),!1)},$t=function(r,p,m){if(Lt&&(p==="id"||p==="name")&&(m in t||m in Ds))return!1;if(!(We&&!qe[p]&&M(_s,p))){if(!(At&&M(Rs,p))){if(!L[p]||qe[p]){if(!(Ut(r)&&(T.tagNameCheck instanceof RegExp&&M(T.tagNameCheck,r)||T.tagNameCheck instanceof Function&&T.tagNameCheck(r))&&(T.attributeNameCheck instanceof RegExp&&M(T.attributeNameCheck,p)||T.attributeNameCheck instanceof Function&&T.attributeNameCheck(p))||p==="is"&&T.allowCustomizedBuiltInElements&&(T.tagNameCheck instanceof RegExp&&M(T.tagNameCheck,m)||T.tagNameCheck instanceof Function&&T.tagNameCheck(m))))return!1}else if(!Xe[p]){if(!M(St,xe(m,kt,""))){if(!((p==="src"||p==="xlink:href"||p==="href")&&r!=="script"&&Ia(m,"data:")===0&&Ot[r])){if(!(_t&&!M(Ls,xe(m,kt,"")))){if(m)return!1}}}}}}return!0},Ut=function(r){return r!=="annotation-xml"&&ts(r,Is)},Gt=function(r){G(N.beforeSanitizeAttributes,r,null);const{attributes:p}=r;if(!p||et(r))return;const m={attrName:"",attrValue:"",keepAttr:!0,allowedAttributes:L,forceKeepAttr:void 0};let k=p.length;for(;k--;){const C=p[k],{name:E,namespaceURI:B,value:q}=C,he=R(E),tt=q;let O=E==="value"?tt:Ca(tt);if(m.attrName=he,m.attrValue=O,m.keepAttr=!0,m.forceKeepAttr=void 0,G(N.uponSanitizeAttribute,r,m),O=m.attrValue,It&&(he==="id"||he==="name")&&(oe(E,r),O=Cs+O),Ee&&M(/((--!?|])>)|<\/(style|title)/i,O)){oe(E,r);continue}if(m.forceKeepAttr)continue;if(!m.keepAttr){oe(E,r);continue}if(!Rt&&M(/\/>/i,O)){oe(E,r);continue}se&&Ne([$e,Ue,Ge],Wt=>{O=xe(O,Wt," ")});const qt=R(r.nodeName);if(!$t(qt,he,O)){oe(E,r);continue}if(A&&typeof S=="object"&&typeof S.getAttributeType=="function"&&!B)switch(S.getAttributeType(qt,he)){case"TrustedHTML":{O=A.createHTML(O);break}case"TrustedScriptURL":{O=A.createScriptURL(O);break}}if(O!==tt)try{B?r.setAttributeNS(B,E,O):r.setAttribute(E,O),et(r)?F(r):es(e.removed)}catch{oe(E,r)}}G(N.afterSanitizeAttributes,r,null)},Bs=function f(r){let p=null;const m=jt(r);for(G(N.beforeSanitizeShadowDOM,r,null);p=m.nextNode();)G(N.uponSanitizeShadowNode,p,null),Ft(p),Gt(p),p.content instanceof i&&f(p.content);G(N.afterSanitizeShadowDOM,r,null)};return e.sanitize=function(f){let r=arguments.length>1&&arguments[1]!==void 0?arguments[1]:{},p=null,m=null,k=null,C=null;if(Ke=!f,Ke&&(f="<!-->"),typeof f!="string"&&!Ht(f))if(typeof f.toString=="function"){if(f=f.toString(),typeof f!="string")throw be("dirty is not a string, aborting")}else throw be("toString is not a function");if(!e.isSupported)return f;if(Ve||Qe(r),e.removed=[],typeof f=="string"&&(pe=!1),pe){if(f.nodeName){const q=R(f.nodeName);if(!_[q]||de[q])throw be("root node is forbidden and cannot be sanitized in-place")}}else if(f instanceof l)p=Bt("<!---->"),m=p.ownerDocument.importNode(f,!0),m.nodeType===we.element&&m.nodeName==="BODY"||m.nodeName==="HTML"?p=m:p.appendChild(m);else{if(!ae&&!se&&!Q&&f.indexOf("<")===-1)return A&&_e?A.createHTML(f):f;if(p=Bt(f),!p)return ae?null:_e?X:""}p&&Ye&&F(p.firstChild);const E=jt(pe?f:p);for(;k=E.nextNode();)Ft(k),Gt(k),k.content instanceof i&&Bs(k.content);if(pe)return f;if(ae){if(Ae)for(C=Ts.call(p.ownerDocument);p.firstChild;)C.appendChild(p.firstChild);else C=p;return(L.shadowroot||L.shadowrootmode)&&(C=As.call(a,C,!0)),C}let B=Q?p.outerHTML:p.innerHTML;return Q&&_["!doctype"]&&p.ownerDocument&&p.ownerDocument.doctype&&p.ownerDocument.doctype.name&&M(ks,p.ownerDocument.doctype.name)&&(B="<!DOCTYPE "+p.ownerDocument.doctype.name+`>
`+B),se&&Ne([$e,Ue,Ge],q=>{B=xe(B,q," ")}),A&&_e?A.createHTML(B):B},e.setConfig=function(){let f=arguments.length>0&&arguments[0]!==void 0?arguments[0]:{};Qe(f),Ve=!0},e.clearConfig=function(){le=null,Ve=!1},e.isValidAttribute=function(f,r,p){le||Qe({});const m=R(f),k=R(r);return $t(m,k,p)},e.addHook=function(f,r){typeof r=="function"&&ge(N[f],r)},e.removeHook=function(f,r){if(r!==void 0){const p=Ra(N[f],r);return p===-1?void 0:La(N[f],p,1)[0]}return es(N[f])},e.removeHooks=function(f){N[f]=[]},e.removeAllHooks=function(){N=ls()},e}var Wa=Ss();class Va{constructor(){this.currentPage="landing",this.appElement=document.querySelector("#app"),this.currentStep=1,this.totalSteps=13,this.setupEarlyAccessEvents(),this.init()}init(){this.setupRouter(),this.render()}setupRouter(){window.addEventListener("hashchange",()=>{this.handleRouteChange()}),this.handleRouteChange()}handleRouteChange(){const e=window.location.hash.slice(1)||"landing";this.currentPage=e,this.render()}render(){switch(this.currentPage){case"landing":this.appElement.innerHTML=Vt();break;case"hormozi-style-headline-generator":this.appElement.innerHTML=Fs(),this.setupHeadlineGeneratorEvents();break;case"early-access":this.appElement.innerHTML=$s(),this.setupEarlyAccessEvents();break;default:this.appElement.innerHTML=Vt()}}setupEarlyAccessEvents(){const e=document.getElementById("start-form"),t=document.getElementById("next-btn"),a=document.getElementById("prev-btn");document.getElementById("submit-btn");const n=document.getElementById("early-access-form");e&&e.addEventListener("click",this.showForm.bind(this)),t&&t.addEventListener("click",this.nextStep.bind(this)),a&&a.addEventListener("click",this.prevStep.bind(this)),n&&n.addEventListener("submit",this.handleFormSubmit.bind(this))}showForm(){const e=document.getElementById("welcome-screen"),t=document.getElementById("form-container");e.classList.add("hidden"),t.classList.remove("hidden"),t.classList.add("fade-in")}nextStep(){this.validateCurrentStep()&&this.currentStep<this.totalSteps&&(this.hideCurrentStep(),this.currentStep++,this.showCurrentStep(),this.updateProgress(),this.updateButtons())}prevStep(){this.currentStep>1&&(this.hideCurrentStep(),this.currentStep--,this.showCurrentStep(),this.updateProgress(),this.updateButtons())}validateCurrentStep(){const e=document.querySelector(`.form-step[data-step="${this.currentStep}"]`),t=e.querySelectorAll("input[required], textarea[required]");for(let i of t){if(!i.value.trim())return i.focus(),this.showError("Please fill in all required fields"),!1;if(i.type==="email"&&!this.validateEmail(i.value))return i.focus(),this.showError("Please enter a valid business email address"),!1;if(i.type==="url"){let c=i.value.trim();if(!/^(https?:\/\/|www\.)/i.test(c))return i.focus(),this.showError("Please enter a valid URL (should start with http://, https://, or www.)"),!1;const l=c.replace(/^((https?:\/\/|www\.)[^\/?#]+).*$/i,"$1");i.value=l.toLowerCase()}}const a=e.querySelectorAll('input[type="radio"][required]'),n=[...new Set([...a].map(i=>i.name))];for(let i of n)if(!e.querySelector(`input[name="${i}"]:checked`))return this.showError("Please select an option"),!1;return!0}validateEmail(e){if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e))return!1;const n=["gmail.com","outlook.com","hotmail.com","yahoo.com","ymail.com","protonmail.com","icloud.com","mail.com","example.com","aol.com","duck.com"],i=e.split("@")[1].toLowerCase();return!n.includes(i)}validateURL(e){try{return e.match(/^https?:\/\//i)||(e="https://"+e),new URL(e),!0}catch{return!1}}hideCurrentStep(){const e=document.querySelector(`.form-step[data-step="${this.currentStep}"]`);e&&(e.classList.remove("active"),e.style.opacity="0",setTimeout(()=>{e.style.display="none"},300))}showCurrentStep(){const e=document.querySelector(`.form-step[data-step="${this.currentStep}"]`);e&&(e.style.display="block",setTimeout(()=>{e.style.opacity="1",e.classList.add("active")},50))}updateProgress(){const e=document.getElementById("progress-bar"),t=this.currentStep/this.totalSteps*100,a=document.getElementById("progress-percent"),n=document.getElementById("progress-text"),i=document.getElementById("current-step");n&&i&&(i.textContent=this.currentStep,n.textContent=`${this.currentStep}`),a&&(a.textContent=`${Math.round(t)}%`),e&&(e.style.width=`${t}%`),document.querySelectorAll(".step").forEach((l,u)=>{u<this.currentStep?l.classList.add("step-primary"):l.classList.remove("step-primary")})}updateButtons(){const e=document.getElementById("next-btn"),t=document.getElementById("prev-btn"),a=document.getElementById("submit-btn");t&&(t.disabled=this.currentStep===1),this.currentStep===this.totalSteps?(e&&e.classList.add("hidden"),a&&a.classList.remove("hidden")):(e&&e.classList.remove("hidden"),a&&a.classList.add("hidden"))}async handleFormSubmit(e){if(e.preventDefault(),!this.validateCurrentStep())return;const t=new FormData(e.target),a=Object.fromEntries(t.entries()),n=new URLSearchParams(window.location.search);["utm_id","utm_source","utm_medium","utm_campaign","utm_term","utm_content","ref"].forEach(l=>{n.has(l)&&(a[l]=n.get(l))}),a.timestamp=new Date().toISOString();const i=document.getElementById("submit-btn"),c=i.innerHTML;i.innerHTML=`
      <span class="loading loading-spinner loading-sm"></span>
      Submitting...
    `,i.disabled=!0;try{const l=new URL("https://script.google.com/macros/s/AKfycbzgO2EG_gIkLvHgeZu3N0uTcd_16ZUrnwUwO29T_FJrtg883JK8tVqTW2sjc0xt_iYf9g/exec");if(l.search=new URLSearchParams(a).toString(),!(await fetch(l,{method:"GET",redirect:"follow"})).ok)throw new Error("Submission failed");this.showThankYou()}catch(l){console.error("Submission error:",l),this.showError("Submission failed. Please try again.")}finally{i.innerHTML=c,i.disabled=!1}}showThankYou(){const e=document.getElementById("form-container"),t=document.getElementById("thank-you-screen");e.classList.add("hidden"),t.classList.remove("hidden"),t.classList.add("fade-in")}setupHeadlineGeneratorEvents(){const e=document.getElementById("user-form"),t=document.getElementById("ai-form");e&&e.addEventListener("submit",this.handleUserSubmit.bind(this)),t&&t.addEventListener("submit",this.handleAISubmit.bind(this))}validateLinkedInURL(e){return/^https?:\/\/(www\.)?linkedin\.com\/in\/[a-zA-Z0-9-]+\/?$/.test(e)}validateBusinessEmail(e){if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(e))return!1;const n=["gmail.com","outlook.com","hotmail.com","yahoo.com","ymail.com","protonmail.com","icloud.com","mail.com","example.com","aol.com","duck.com"],i=e.split("@")[1].toLowerCase();return!n.includes(i)}showFieldError(e,t){const a=document.getElementById(e),n=document.getElementById(`${e}-error`),i=n.querySelector(".label-text-alt");a.classList.add("input-error"),i.textContent=t,n.classList.remove("hidden")}clearFieldError(e){const t=document.getElementById(e),a=document.getElementById(`${e}-error`);t.classList.remove("input-error"),a.classList.add("hidden")}clearAllErrors(){["name","linkedin","email"].forEach(e=>{this.clearFieldError(e)})}validateUserForm(e){var c;this.clearAllErrors();let t=!0;const a=e.get("name"),n=e.get("linkedin"),i=e.get("email");if((!a||a.trim().length<2)&&(this.showFieldError("name","Please enter a valid full name"),t=!1),(!n||!this.validateLinkedInURL(n))&&(this.showFieldError("linkedin","Please enter a valid LinkedIn profile URL (e.g., https://linkedin.com/in/your-profile)"),t=!1),!i||!this.validateBusinessEmail(i)){if(i){const l=(c=i.split("@")[1])==null?void 0:c.toLowerCase();l&&["gmail.com","outlook.com","hotmail.com","yahoo.com","ymail.com","protonmail.com","icloud.com","mail.com","example.com","aol.com","duck.com"].includes(l)?this.showFieldError("email",`Email addresses from ${l} are not accepted. Please use your business email.`):this.showFieldError("email","Please enter a valid business email address")}else this.showFieldError("email","Please enter a valid business email address");t=!1}return t}async handleUserSubmit(e){e.preventDefault();const t=new FormData(e.target);if(!this.validateUserForm(t))return;const a={full_name:t.get("name"),email:t.get("email"),linkedin:t.get("linkedin")},n=e.target.querySelector('button[type="submit"]'),i=n.innerHTML;n.innerHTML=`
      <span class="loading loading-spinner loading-sm"></span>
      Submitting...
    `,n.disabled=!0;try{(await(await fetch("https://outreach.gatara.org/api/submit/",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(a)})).json()).success?this.showAIForm():this.showError("Submission failed. Please try again.")}catch{this.showError("Network error. Please check your connection and try again.")}finally{n.innerHTML=i,n.disabled=!1}}async handleAISubmit(e){e.preventDefault();const t=new FormData(e.target),a={email_content:t.get("email_content"),target_audience:t.get("target_audience"),tone_of_voice:t.get("tone_of_voice"),main_pain:t.get("main_pain"),outcome:t.get("outcome")};this.showLoader();try{const i=await(await fetch("https://outreach.gatara.org/api/ai-response/",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(a)})).json();this.showResult(i.result)}catch{this.showError("AI processing failed. Please try again.")}}showAIForm(){const e=document.getElementById("user-section"),t=document.getElementById("ai-section");e.classList.add("hidden"),t.classList.remove("hidden"),t.classList.add("fade-in"),t.scrollIntoView({behavior:"smooth"})}showLoader(){const e=document.getElementById("ai-section"),t=document.getElementById("loader-section");e.classList.add("hidden"),t.classList.remove("hidden"),t.classList.add("fade-in"),t.scrollIntoView({behavior:"smooth"})}showResult(e){const t=document.getElementById("loader-section"),a=document.getElementById("result-section");t.classList.add("hidden");const i=(typeof e=="string"?e:(e==null?void 0:e.result)||"⚠️ Invalid response format").replace(/(Pair \d+) (Subject: )?(.*?) (Headline: )?(.*?)(\n|$)/g,`$1
- Subject:
$3
- Headline:
$5
`),c=Wa.sanitize(v.parse(i));a.innerHTML=`
      <div class="card bg-base-100 shadow-2xl">
        <div class="card-body p-8">
          <div class="text-center mb-8">
            <h2 class="text-4xl font-bold text-base-content mb-4">Your Hormozi-Style Headlines & Subjects</h2>
            <div class="badge badge-success badge-lg">Generated Successfully!</div>
          </div>
          <div class="bg-base-200 rounded-lg p-6 mb-8 text-lg leading-relaxed whitespace-pre-line [&>p]:my-4">
            ${c}
          </div>
          <div class="text-center">
            <button onclick="window.location.href = '/'" class="btn btn-primary btn-lg gap-2">
              <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
              </svg>
              Go Back Home ;)
            </button>
          </div>
        </div>
      </div>
    `,a.classList.remove("hidden"),a.classList.add("fade-in"),a.scrollIntoView({behavior:"smooth"})}showError(e){const t=document.createElement("div");t.className="toast toast-top toast-end z-50",t.innerHTML=`
      <div class="alert alert-error">
        <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
        <span>${e}</span>
      </div>
    `,document.body.appendChild(t),setTimeout(()=>{t.remove()},5e3)}}new Va;
