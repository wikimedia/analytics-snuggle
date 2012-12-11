UI = UI || {}

UI.Dropper = Class.extend({
	init: function(tab, content){
		this.node = $("<div>")
			.addClass("dropper")
		
		this.tab = {
			node: $("<div>")
				.addClass("tab")
				.append($("<span>").append(tab || ""))
				.click(this._handle_tab_click.bind(this))
		}
		this.node.append(this.tab.node)
		
		this.pane = {
			node: $("<div>")
				.addClass("pane")
				.append(content || "")
				.hide()
				.click(function(e){e.stopPropagation()})
		}
		this.node.append(this.pane.node)
		
		//This is experimental.  I'm not sure if it is kosher.
		//Hopefully, if you click on something that doesn't capture the 
		//click event, it will bubble up to the body and then we can 
		//know to close the dropper. 
		$("body").click(function(e){this.expanded(false)}.bind(this))
		
		this.expanded(false)
	},
	_handle_tab_click: function(e){
		this.expanded(!this.expanded())
		e.stopPropagation()
	},
	expanded: function(expanded){
		if(expanded === undefined){
			return this.pane.node.hasClass("expanded")
		}else{
			if(expanded){
				this.pane.node.addClass("expanded")
				this.pane.node.slideDown(200)
			}else{
				this.pane.node.slideUp(
					200,
					function(){
						this.pane.node.removeClass("expanded")
					}.bind(this)
				)
			}
		}
	},
	set_content: function(content){
		this.pane.node.html("") //Clear out the old content
		this.pane.node.append(content || "")
	}
})

