# EMNLP 2019 official website

This is the code for the official website for the Conference on Empirical Methods in Natural Language Processing & International Joint Conference on Natural Language Processing 2019 (EMNLP-IJCNLP 2019). 

The code is based on the code of the EMNLP 2018 developed by Nitin Madnani. It has been adapted and extended by Kevin Duh and Henning Wachsmuth for EMNLP-IJCNLP 2019.


## Website basis

The website is currently using the [Minimal Mistakes Jekyll Theme](https://mmistakes.github.io/minimal-mistakes/).

You can test this website locally on OS X as follows:

1. Install bundler: `sudo gem install bundler`. Make sure you have Ruby and Bundler versions > 2.4.
2. Check out this repository.
3. Run the gems needed by this repository: `sudo bundle install`. 
   *Note*: This step might fail when installing the `nokogiri` gem. If this happens, run `bundle config build.nokogiri --use-system-libraries` and then run `bundle install` again.
4. Start the jekyll server by running `bundle exec jekyll serve`.
5. You can then see the website at http://localhost:4000.


## Domain set-up

The following settings connect the the main domain booked for the conference (here assuming emnlp-ijcnlp2019.org) with the underlying webspace (here assuming the website is hosted on Github). The connection is done in a way, such that it the main domain (with preceding "www.") is shown in the URL field of a browser, but the appended relative paths (e.g., "/organization") are taken from the webspace.

On the domain side, the following DNS settings needed to be set up. All four IPs belong to Github, the last row connects the www subdomain to the main domain:
	
   A	  @	    185.199.108.153	
   A	  @	    185.199.109.153		
   A	  @	    185.199.110.153		
   A	  @	    185.199.111.153		
   CNAME  www	emnlp-ijcnlp2019.org

In the Github page settings, the "custom domain" needs to be set to the main domain. This will create a CNAME file in the top folder of the Github repository.

That's it. Notice that changes may take some minutes until they get effective online.


## License

The MIT License (MIT)

Copyright (c) 2017 Association for Computational Linguistics.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
