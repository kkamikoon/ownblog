!function(f) {
    "use strict";
    function m(t, e, a, i, n) {
        if (e.length) {
            n.show();
            var o = new FormData
              , d = 0;
            for (d = 0; d < e.length; d++)
                o.append("file" + d, e[d]);
            f.ajax({
                url: t,
                type: "POST",
                contentType: !1,
                data: o,
                processData: !1,
                cache: !1,
                dataType: "json",
                // custom - kkamikoon
                complete: function(uploadedPath){
                    i.insertSnippet(a, uploadedPath.responseText);
                }
            }).done(function(t) {
                var e = "";
                1 < t.length && (e = "\n");
                for (var n = 0; n < t.length; n++)
                    i.insertSnippet(a, "![](" + t[n] + ")" + e)
            }).always(function() {
                n.hide()
            })
        }
    }
    function g(t) {
        var e, n = f(window).height(), a = t.offset().top;
        a < n && (e = n - a,
        t.css("height", e + "px"))
    }
    function h(t, e) {
        0 === t.getCursorPosition().column ? (t.navigateLineStart(),
        t.insert(e + " ")) : (t.navigateLineStart(),
        t.insert(e + " "),
        t.navigateLineEnd())
    }
    var e = {
        init: function(t) {
            var n, e, a, i, o = f.extend(!0, {}, f.fn.markdownEditor.defaults, t), d = this, s = !1, l = !1;
            d.addClass("md-textarea-hidden"),
            n = f("<div/>"),
            d.after(n),
            n.addClass("md-container").html((e = d.val(),
            i = "",
            i += '<div class="md-loading"><span class="md-icon-container"><span class="md-icon"></span></span></div>',
            i += '<div class="md-toolbar">',
            i += '<div class="btn-toolbar">',
            i += '<div class="btn-group">',
            i += '<button type="button" data-mdtooltip="tooltip" title="' + (a = o).label.btnHeader1 + '" class="md-btn btn btn-outline-secondary" data-btn="h1">H1</button>',
            i += '<button type="button" data-mdtooltip="tooltip" title="' + a.label.btnHeader2 + '" class="md-btn btn btn-outline-secondary" data-btn="h2">H2</button>',
            i += '<button type="button" data-mdtooltip="tooltip" title="' + a.label.btnHeader3 + '" class="md-btn btn btn-outline-secondary" data-btn="h3">H3</button>',
            i += "</div>",
            i += '<div class="btn-group">',
            i += '<button type="button" data-mdtooltip="tooltip" title="' + a.label.btnBold + '" class="md-btn btn btn-outline-secondary" data-btn="bold"><span class="fas fa-bold"></span></button>',
            i += '<button type="button" data-mdtooltip="tooltip" title="' + a.label.btnItalic + '" class="md-btn btn btn-outline-secondary" data-btn="italic"><span class="fas fa-italic"></span></button>',
            i += "</div>",
            i += '<div class="btn-group">',
            i += '<button type="button" data-mdtooltip="tooltip" title="' + a.label.btnList + '" class="md-btn btn btn-outline-secondary" data-btn="ul"><span class="fas fa-list"></span></button>',
            i += '<button type="button" data-mdtooltip="tooltip" title="' + a.label.btnOrderedList + '" class="md-btn btn btn-outline-secondary" data-btn="ol"><span class="fas fa-list-ol"></span></button>',
            i += "</div>",
            i += '<div class="btn-group">',
            i += '<button type="button" data-mdtooltip="tooltip" title="' + a.label.btnLink + '" class="md-btn btn btn-outline-secondary" data-btn="link"><span class="fas fa-link"></span></button>',
            i += '<button type="button" data-mdtooltip="tooltip" title="' + a.label.btnImage + '" class="md-btn btn btn-outline-secondary" data-btn="image"><span class="fas fa-image"></span></button>',
            !0 === a.imageUpload && (i += '<div data-mdtooltip="tooltip" title="' + a.label.btnUpload + '" class="btn btn-outline-secondary md-btn-file"><span class="fas fa-upload"></span><input class="md-input-upload" type="file" multiple accept=".jpg,.jpeg,.png,.gif"></div>'),
            i += "</div>",
            !0 === a.fullscreen && (i += '<div class="btn-group">',
            // i += '<button type="button" class="md-btn btn btn-outline-secondary" data-btn="fullscreen"><span class="fas fa-expand-arrows-alt"></span> ' + a.label.btnFullscreen + "</button>",
            i += "</div>"),
            !0 === a.preview && (i += '<div class="btn-group">',
            i += '<button type="button" class="md-btn btn btn-outline-secondary btn-edit active" data-btn="edit"><span class="fas fa-edit"></span> ' + a.label.btnEdit + "</button>",
            i += '<button type="button" class="md-btn btn btn-outline-secondary btn-preview" data-btn="preview"><span class="fas fa-eye"></span> ' + a.label.btnPreview + "</button>",
            i += "</div>"),
            i += '<div class="btn-group ml-auto">', // Submit Button - kkamikoon
            i += '<button type="submit" data-mdtooltip="tooltip" title="' + a.label.Submit + '" class="md-btn btn btn-outline-warning">Submit</button>',
            i += "</div>",
            i += "</div>",
            i += "</div>",
            i += '<div class="md-editor">' + f("<div>").text(e).html() + "</div>",
            i += '<div class="md-preview" style="display:none"></div>')),
            "function" == typeof f().tooltip && n.find('[data-mdtooltip="tooltip"]').tooltip({
                container: "body"
            });
            var b = n.find(".md-editor")
              , r = n.find(".md-preview")
              , p = n.find(".md-loading");
            n.css({
                width: o.width
            }),
            b.css({
                height: o.height,
                fontSize: o.fontSize
            }),
            r.css({
                height: o.height
            });
            var c, u = ace.edit(b[0]);
            return u.setTheme("ace/theme/" + o.theme),
            u.getSession().setMode("ace/mode/markdown"),
            u.getSession().setUseWrapMode(!0),
            u.getSession().setUseSoftTabs(o.softTabs),
            u.getSession().on("change", function() {
                d.val(u.getSession().getValue())
            }),
            u.setHighlightActiveLine(!1),
            u.setShowPrintMargin(!1),
            u.renderer.setShowGutter(!1),
            ace.config.loadModule("ace/ext/language_tools", function() {
                var t, n;
                c = ace.require("ace/snippets").snippetManager,
                n = c,
                (t = u).commands.addCommand({
                    name: "bold",
                    bindKey: {
                        win: "Ctrl-B",
                        mac: "Command-B"
                    },
                    exec: function(t) {
                        var e = t.session.getTextRange(t.getSelectionRange());
                        "" === e ? n.insertSnippet(t, "**${1:text}**") : n.insertSnippet(t, "**" + e + "**")
                    },
                    readOnly: !1
                }),
                t.commands.addCommand({
                    name: "italic",
                    bindKey: {
                        win: "Ctrl-I",
                        mac: "Command-I"
                    },
                    exec: function(t) {
                        var e = t.session.getTextRange(t.getSelectionRange());
                        "" === e ? n.insertSnippet(t, "*${1:text}*") : n.insertSnippet(t, "*" + e + "*")
                    },
                    readOnly: !1
                }),
                t.commands.addCommand({
                    name: "link",
                    bindKey: {
                        win: "Ctrl-K",
                        mac: "Command-K"
                    },
                    exec: function(t) {
                        var e = t.session.getTextRange(t.getSelectionRange());
                        "" === e ? n.insertSnippet(t, "[${1:text}](http://$2)") : n.insertSnippet(t, "[" + e + "](http://$1)")
                    },
                    readOnly: !1
                })
            }),
            o.imageUpload && (n.find(".md-input-upload").on("change", function() {
                var t = f(this).get(0).files;
                m(o.uploadPath, t, u, c, p);
            }),
            n.on("dragenter", function(t) {
                t.stopPropagation(),
                t.preventDefault()
            }),
            n.on("dragover", function(t) {
                t.stopPropagation(),
                t.preventDefault()
            }),
            n.on("drop", function(t) {
                t.preventDefault();
                var e = t.originalEvent.dataTransfer.files;
                m(o.uploadPath, e, u, c, p)
            })),
            !0 === o.fullscreen && f(window).resize(function() {
                !0 === l && g(!1 === s ? b : r)
            }),
            n.find(".md-btn").click(function() {
                var t = f(this).data("btn")
                  , e = u.session.getTextRange(u.getSelectionRange());
                "h1" === t ? h(u, "#") : "h2" === t ? h(u, "##") : "h3" === t ? h(u, "###") : "ul" === t ? h(u, "*") : "ol" === t ? h(u, "1.") : "bold" === t ? u.execCommand("bold") : "italic" === t ? u.execCommand("italic") : "link" === t ? u.execCommand("link") : "image" === t ? "" === e ? c.insertSnippet(u, "![${1:text}](http://$2)") : c.insertSnippet(u, "![" + e + "](http://$1)") : "edit" === t ? (s = !1,
                r.hide(),
                b.show(),
                n.find(".btn-edit").addClass("active"),
                n.find(".btn-preview").removeClass("active"),
                !0 === l && g(b)) : "preview" === t ? (s = !0,
                r.html('<p style="text-align:center; font-size:16px">' + o.label.loading + "...</p>"),
                o.onPreview(u.getSession().getValue(), function(t) {
                    r.html(t)
                }),
                b.hide(),
                r.show(),
                n.find(".btn-preview").addClass("active"),
                n.find(".btn-edit").removeClass("active"),
                !0 === l && g(r)) : "fullscreen" === t && (!0 === l ? (l = !1,
                f("body, html").removeClass("md-body-fullscreen"),
                n.removeClass("md-fullscreen"),
                b.css("height", o.height),
                r.css("height", o.height)) : (l = !0,
                f("body, html").addClass("md-body-fullscreen"),
                n.addClass("md-fullscreen"),
                g(!1 === s ? b : r)),
                u.resize()),
                u.focus()
            }),
            this
        },
        content: function() {
            return ace.edit(this.find(".md-editor")[0]).getSession().getValue()
        },
        setContent: function(t) {
            ace.edit(this.find(".md-editor")[0]).setValue(t, 1)
        }
    };
    f.fn.markdownEditor = function(t) {
        return e[t] ? e[t].apply(this, Array.prototype.slice.call(arguments, 1)) : "object" != typeof t && t ? void f.error("Method " + t + " does not exist on jQuery.markdownEditor") : e.init.apply(this, arguments)
    }
    ,
    f.fn.markdownEditor.defaults = {
        width: "100%",
        height: "400px",
        fontSize: "14px",
        theme: "tomorrow",
        softTabs: !0,
        fullscreen: !0,
        imageUpload: !1,
        uploadPath: "",
        preview: !1,
        onPreview: function(t, e) {
            e(t)
        },
        label: {
            btnHeader1: "Header 1",
            btnHeader2: "Header 2",
            btnHeader3: "Header 3",
            btnBold: "Bold",
            btnItalic: "Italic",
            btnList: "Unordered list",
            btnOrderedList: "Ordered list",
            btnLink: "Link",
            btnImage: "Insert image",
            btnUpload: "Upload image",
            btnEdit: "Edit",
            btnPreview: "Preview",
            // btnFullscreen: "Fullscreen",
            loading: "Loading",
            submit: "Submit"
        }
    }
}(jQuery);
//# sourceMappingURL=bootstrap-markdown-editor.min.js.map
