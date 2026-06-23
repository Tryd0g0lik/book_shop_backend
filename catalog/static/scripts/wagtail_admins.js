// catalog/static/scripts/wagtail_admin_js.js:1


function customForm() {
	const boxHtml = document.querySelector(".custom-property-value");
	if (boxHtml === null) return;
	
	const inlineChildPropertyHtmlAll = boxHtml.querySelectorAll("[id^='inline_child_']");
	
	
	if (inlineChildPropertyHtmlAll !== null || inlineChildPropertyHtmlAll.length !== 0) {
		inlineChildPropertyHtmlAll.forEach((item, i) =>{
			const buttomHTMLAll = boxHtml.querySelectorAll("button.w-panel__toggle");
			item.setAttribute("hidden","until-found");
			buttomHTMLAll[i].setAttribute("aria-expanded", false);
			
			
		});
		
	}
	console.log("Hallo Wagtail");
};
document.removeEventListener("DOMContentLoaded", () => customForm());
document.addEventListener("DOMContentLoaded", () => customForm());
