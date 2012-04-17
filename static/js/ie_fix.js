Prototype.Browser.IE6 = Prototype.Browser.IE && parseInt(navigator.userAgent.substring(navigator.userAgent.indexOf("MSIE")+5)) == 6;
Prototype.Browser.IE7 = Prototype.Browser.IE && parseInt(navigator.userAgent.substring(navigator.userAgent.indexOf("MSIE")+5)) == 7;
Prototype.Browser.IE8 = Prototype.Browser.IE && !Prototype.Browser.IE6 && !Prototype.Browser.IE7;

var IEDropdown = Class.create({
    initialize: function(element) {
        this.element = $(element);
        this.originalWidth = this.element.style.width;
        this.dontWiden = false;
        Event.observe(this.element, 'mousedown', this.widen.bindAsEventListener(this));
        Event.observe(this.element, 'blur', this.shrink.bindAsEventListener(this));
        Event.observe(this.element, 'change', this.shrink.bindAsEventListener(this));
    },


    widen: function(e) {
        if(this.dontWiden) return;
        var styledWidth = this.element.offsetWidth;
        this.element.style.width = 'auto';
        var desiredWidth = this.element.offsetWidth;
        // If this control needs less than it was styled for, then we don't need to bother with widening it.
        if(desiredWidth < styledWidth) {
           this.dontWiden = true;
           this.element.style.width = this.originalWidth;
           this.element.click(); // Simulate another click, since setting styles has already caused the box to close at this point.
        }
    },

    shrink: function(e) {
        this.element.style.width = this.originalWidth;
    }
});

