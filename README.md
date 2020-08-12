## ojisanseiuchi.com source code  

This is the source code for the site [www.ojisanseiuchi.com](http://www.ojisanseiuchi.com), the personal weblog of Alan Duncan. 

The site is built using [Hugo](https://gohugo.io/), a static site generating platform and styled with a heavily modified version of the [Mainroad](https://github.com/Vimux/Mainroad) theme. The theme is **not** a submodule of this project. It's just easier for me to manage when everything is all integrated. Besides, I'm not planning on reusing this theme in any other project. So why not?

### Usage

#### Creating new post

To create a new post: `hugo new post/yyy-mm-dd-your-title/index.md`

#### Building the site

To build the site and serve it locally for testing: `hugo server -D` or to build for deployment, just `hugo`.

#### Deployment

There is currently no facility for deploying the site. Simply build and use Transmit to upload the `public` directory.

### Development notes

- Uses the built-in [syntax highlighting](https://gohugo.io/content-management/syntax-highlighting/#readout), which uses [Chroma](https://github.com/alecthomas/chroma). Since I want to use a specific theme, the configuration parameter `pygmentsUseClasses = true` is set in the site configuration file. The site is currently using the [Monokai light](https://xyproto.github.io/splash/docs/monokailight.html) style. Note that the syntax.css file is expected in static/css/syntax.css and has to be built from the Chroma style: `hugo gen chromastyles --style=monokailight > syntax.css` then just move the generated css file into place.

### References

- [Chroma styles](https://xyproto.github.io/splash/docs/) - syntax highlighter styles
- [Chroma syntax highlighter](https://github.com/alecthomas/chroma) - project page for the syntax highlighter in use by Hugo.
- [Hugo syntax highlighting](https://gohugo.io/content-management/syntax-highlighting/#readout) - documentation page for Hugo syntax colouring
