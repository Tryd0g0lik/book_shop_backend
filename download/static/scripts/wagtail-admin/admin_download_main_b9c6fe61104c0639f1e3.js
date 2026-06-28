/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./src/functions.ts"
/*!**************************!*\
  !*** ./src/functions.ts ***!
  \**************************/
(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

eval("{__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   publishButtomDownloadCatalog: () => (/* binding */ publishButtomDownloadCatalog)\n/* harmony export */ });\n// download\\src\\functions.ts\n\nfunction publishButtomDownloadCatalog() {\n  /**\n   * Admin Wagtail's interface receiving a (html block ) buttom ('<button type=\"button\" data-name=\"download-catalog\" ...>') for a download XLS file.\n   * This function is a filter for this buttom.\n   * We can see it only on the page of catalog of product (publish her).\n   */\n  const regex_catalog = /(admin\\/catalog\\/\\products\\/)/;\n  const regex_product_edit = /((admin\\/catalog\\/products\\/)(edit\\/[0-1]+\\/?))/;\n  const buttomHtml = document.querySelector(\"[data-name='download-catalog']\");\n  if (!buttomHtml) return;\n  if (!window.location.href.match(regex_catalog) && !window.location.href.match(regex_product_edit)) {\n    buttomHtml.remove();\n  }\n}\n;\n\n\n//# sourceURL=webpack://shoop-admin-download/./src/functions.ts?\n}");

/***/ },

/***/ "./src/index.ts"
/*!**********************!*\
  !*** ./src/index.ts ***!
  \**********************/
(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

eval("{__webpack_require__.r(__webpack_exports__);\n/* harmony import */ var _load_catalog_functions__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! ./load_catalog/functions */ \"./src/load_catalog/functions.ts\");\n/* harmony import */ var _functions__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./functions */ \"./src/functions.ts\");\n// download\\src\\index.ts\n\n\ndocument.removeEventListener(\"DOMContentLoaded\", async () => {\n  // EVENT LISTENER\n  try {\n    // EVENT DOM DOWNLOAD\n    (0,_functions__WEBPACK_IMPORTED_MODULE_1__.publishButtomDownloadCatalog)();\n    // eVENT MOUSDOWN\n    await (0,_load_catalog_functions__WEBPACK_IMPORTED_MODULE_0__.asyncModalwindow)();\n  } catch (error) {\n    console.error(error);\n  }\n});\ndocument.addEventListener(\"DOMContentLoaded\", async () => {\n  try {\n    (0,_functions__WEBPACK_IMPORTED_MODULE_1__.publishButtomDownloadCatalog)();\n    await (0,_load_catalog_functions__WEBPACK_IMPORTED_MODULE_0__.asyncModalwindow)();\n  } catch (error) {\n    console.error(error);\n  }\n});\n\n//# sourceURL=webpack://shoop-admin-download/./src/index.ts?\n}");

/***/ },

/***/ "./src/load_catalog/functions.ts"
/*!***************************************!*\
  !*** ./src/load_catalog/functions.ts ***!
  \***************************************/
(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

eval("{__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   asyncModalwindow: () => (/* binding */ asyncModalwindow)\n/* harmony export */ });\n/* harmony import */ var ___WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! . */ \"./src/load_catalog/index.ts\");\n// download\\src\\load_catalog\\functuions.ts\n// This file performs following tasks:\n// - open a modal window;\n// - sending files;\n// - close a modal window.\n\n\nconst asyncModalwindow = async () => {\n  /**\n   * We should get a html block in main html block on the admin 'Catalog' page.\n   * This is additional interfecae for a load the XLS file to the cataloc.\n   */\n  const modalwondow = new ___WEBPACK_IMPORTED_MODULE_0__.ModalWindow();\n  modalwondow.templatePath = \"static/modal_pages/confirm_convert_alias.txt\";\n  const mainHtml = document.querySelector(\"main[id='main'] header div[class='right']\");\n  if (!mainHtml) return;\n\n  // It listener a click on a buttom in main html block - it is a form for\n  //  a load XLS file to the product catalog.\n  mainHtml.onmousedown = async event => {\n    try {\n      // OPEN FORM\n      // Read the template of modal window (*.txt file).\n      const modalFormStr = await modalwondow.asyncLoadTemplateOfModalWindow(event);\n      if (!modalFormStr) return;\n      // Show/publicaion the modal window.\n      await modalwondow.asyncShowModalWindow(mainHtml, modalFormStr);\n      const zoneHTML = document.querySelector(\"div.drop-zone[id='download-drop-zone']\");\n      if (!zoneHTML) return;\n      // It is a button for close the modal window. It is inside of the modal window body.\n      const divHtml = zoneHTML.querySelector(\"#download-drop-zone p + div\");\n      if (divHtml) {\n        // CLOSE FORM\n        divHtml.onmousedown = event => {\n          let currentTarget = event.currentTarget;\n          if (!currentTarget) return;\n          while (currentTarget && !currentTarget.id && currentTarget.id !== \"download-drop-zone\") {\n            currentTarget = currentTarget.parentElement;\n          }\n          currentTarget.remove();\n        };\n      }\n      ;\n\n      // SEND FILE - listeners of Events &\n      // It is a drop zone for a load XLS file to the server.\n      modalwondow.dropZone(zoneHTML);\n    } catch (error) {\n      console.error(error);\n    }\n  };\n};\n\n\n//# sourceURL=webpack://shoop-admin-download/./src/load_catalog/functions.ts?\n}");

/***/ },

/***/ "./src/load_catalog/index.ts"
/*!***********************************!*\
  !*** ./src/load_catalog/index.ts ***!
  \***********************************/
(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

eval("{__webpack_require__.r(__webpack_exports__);\n/* harmony export */ __webpack_require__.d(__webpack_exports__, {\n/* harmony export */   ModalWindow: () => (/* binding */ ModalWindow)\n/* harmony export */ });\nfunction _defineProperty(e, r, t) { return (r = _toPropertyKey(r)) in e ? Object.defineProperty(e, r, { value: t, enumerable: !0, configurable: !0, writable: !0 }) : e[r] = t, e; }\nfunction _toPropertyKey(t) { var i = _toPrimitive(t, \"string\"); return \"symbol\" == typeof i ? i : i + \"\"; }\nfunction _toPrimitive(t, r) { if (\"object\" != typeof t || !t) return t; var e = t[Symbol.toPrimitive]; if (void 0 !== e) { var i = e.call(t, r || \"default\"); if (\"object\" != typeof i) return i; throw new TypeError(\"@@toPrimitive must return a primitive value.\"); } return (\"string\" === r ? String : Number)(t); }\n// download\\src\\load_catalog\\index.ts\n\n// Send (from an admin's catalog) a file to the server.\nconst pathname = \"/download/files/\";\nclass ModalWindow {\n  constructor() {\n    _defineProperty(this, \"__templatePathname\", void 0);\n    _defineProperty(this, \"logTemplText\", void 0);\n    _defineProperty(this, \"__sizeFile\", 1024);\n    _defineProperty(this, \"__textButtomOfForm\", void 0);\n  }\n  constructionor() {\n    /**\n     * @param __templatePathname: string | undefined - path to a template html/txt file. This is the 'confirm_convert_alias.txt' now.\n     * @param logTemplText: string - Prefix for a tex log.\n     */\n    this.__templatePathname = undefined;\n    this.logTemplText = \"[ModalWindow]\";\n    this.__textButtomOfForm = \"Download\";\n  }\n  static __getClassName() {\n    return this.name;\n  }\n  set templatePath(value) {\n    this.__templatePathname = value;\n  }\n  get templatePath() {\n    return this.__templatePathname;\n  }\n  async asyncLoadTemplateOfModalWindow(event) {\n    /**\n     * Open a modal window.\n     * We have a task  it read a template HTML/txt file and send it next handlers.\n     * This html file is location by a server path - 'templatePath' or can inser new template whem we initional the ModalWindow's obj.\n     * @param event: MouseEvent.\n     * @returns Promise<string | undefined> or err.\n     */\n    const regex = /(\\.txt|\\.html)$/i;\n    try {\n      let target = event.target;\n      if (!target) return;\n      while (!target.hasAttribute(\"data-name\") && target.getAttribute(\"name\") !== \"download-catalog\") {\n        target = target.parentElement;\n      }\n      const dataName = target.getAttribute(\"data-name\");\n      if (!dataName) return;\n      if (dataName.toLowerCase() !== \"download-catalog\") return;\n      // Read the template HTML/txt of file.\n      if (!regex.test(this.templatePath)) throw new Error(`[${this.logTemplText}][${this.asyncLoadTemplateOfModalWindow.name}]: ${{\n        \"cause\": \"Template path is not a valid file!\"\n      }}`);\n      const file_ = await fetch(window.location.origin + \"/\" + this.templatePath);\n      if (!file_.ok) {\n        new Error(`[${this.logTemplText}][${this.asyncLoadTemplateOfModalWindow.name}]: Templete html, for reciving modal html block was hot found!`);\n      }\n      ;\n      return await file_.text();\n    } catch (error) {\n      if (error instanceof Error) {\n        if (error.message.includes(`${this.logTemplText}`)) {\n          throw new Error(`[${this.logTemplText}][${this.asyncLoadTemplateOfModalWindow.name}]: ${{\n            \"cause\": error\n          }}`);\n        } else {\n          throw new Error(`${{\n            \"cause\": error.message\n          }}`);\n        }\n        // removed by dead control flow\n\n      }\n    }\n  }\n  async asyncShowModalWindow(parentHtml, bodyStr) {\n    /**\n     *\n     * We have a task  it show a modal window with a html block.\n     * @param parentHtml: HTMLElement - parent html block for a modal window.\n     * @param bodyStr: string - html content of modal window for a html parent.\n     * @returns Promis<void> or err.\n     */\n    try {\n      parentHtml.insertAdjacentHTML(\"afterbegin\", bodyStr);\n    } catch (error) {\n      if (error instanceof Error) {\n        throw new Error(`[${this.logTemplText}][${this.asyncShowModalWindow.name}]: ${{\n          \"cause\": error\n        }}`);\n      }\n      ;\n    }\n  }\n  async dropZone(dropZone) {\n    const formHtml = dropZone.querySelector(`form[action='${pathname}']`);\n    if (!formHtml) return;\n    // else if ((formHtml as HTMLFormElement).files.length === 0) return;\n    // Drap&Drop - File entering to the zone of drop\n    dropZone.removeEventListener(\"dragenter\", event => {\n      event.preventDefault();\n    });\n    dropZone.addEventListener(\"dragenter\", event => {\n      event.preventDefault();\n    });\n    dropZone.removeEventListener(\"dragover\", event => {\n      event.preventDefault();\n    });\n    dropZone.addEventListener(\"dragover\", event => {\n      event.preventDefault();\n    });\n\n    // Drap&Drop - File exit from the zone of drop\n    dropZone.removeEventListener(\"dragleave\", event => {\n      event.preventDefault();\n    });\n    dropZone.addEventListener(\"dragleave\", event => {\n      event.preventDefault();\n    });\n    // Drap&Drop - File drop\n    dropZone.removeEventListener(\"drop\", async event => {\n      event.preventDefault();\n      await this.handlerOfDrapDropForm(event);\n    });\n    dropZone.addEventListener(\"drop\", async event => {\n      /**\n       * Drap&Drop - Here we get data from a browser.\n       */\n      event.preventDefault();\n      await this.handlerOfDrapDropForm(event);\n    });\n    // ---\n\n    formHtml.removeEventListener(\"mousedown\", event => {\n      this.handlerEventsForm(event);\n    });\n    formHtml.addEventListener(\"mousedown\", event => {\n      this.handlerEventsForm(event);\n    });\n    formHtml.removeEventListener(\"keydown\", event => {\n      this.handlerEventsForm(event);\n    });\n    formHtml.addEventListener(\"keydown\", event => {\n      this.handlerEventsForm(event);\n    });\n    formHtml.removeEventListener(\"submit\", event => {\n      this.handlerEventsForm(event);\n    });\n    formHtml.addEventListener(\"submit\", event => {\n      this.handlerEventsForm(event);\n    });\n    formHtml.removeEventListener(\"change\", event => {\n      this.handlerEventsForm(event);\n    });\n    formHtml.addEventListener(\"change\", event => {\n      this.handlerEventsForm(event);\n    });\n  }\n  async handlerOfDrapDropForm(event) {\n    const files = event.dataTransfer?.files;\n    if (!files) return;\n    // Receive data of forms.\n\n    try {\n      const formData = this.handlerFilesOfForm(files, this.__sizeFile);\n      if (!formData) return;\n      // --- SEND FILES TO THE SERVER.\n      await this.requestPost(formData);\n    } catch (error) {\n      if (error instanceof Error) {\n        throw new Error(`[${this.logTemplText}][${this.dropZone.name}]: ${{\n          \"cause\": error\n        }}`);\n      }\n      ;\n    }\n  }\n  async handlerEventsForm(event) {\n    /**\n     * This method is collection of handlers od forms &  method dropZone (below) it is collection handlers of events.\n     */\n    try {\n      const keyboardKey = event.key;\n      const typeEvent = event.type.toLowerCase();\n      if (typeEvent !== \"submit\" && typeEvent === \"mousedown\" && event.target.tagName.toLowerCase() !== \"input\" && keyboardKey && keyboardKey.toLowerCase() !== \"enter\" && keyboardKey.toLowerCase() !== \"escape\") return;\n      const files = event.target.files;\n      if (!files || files.length === 0) return;\n      // Chenge a text of buttom 1 / 2\n      this.__handlerOfButtom(event, \"Sending\");\n      // --- RECEIVE DATA OF FORMS.\n      const formData = this.handlerFilesOfForm(files, this.__sizeFile);\n      if (!formData) return;\n      // --- SEND FILES TO THE SERVER.\n      const responce = await this.requestPost(formData);\n      // Change a text of buttom 2 / 2\n      if (!responce) {\n        this.__handlerOfButtom(event, \"Error\");\n        return;\n      }\n      ;\n      this.__handlerOfButtom(event, this.__textButtomOfForm);\n    } catch (error) {\n      if (error instanceof Error) {\n        throw new Error(`[${this.logTemplText}][${this.handlerEventsForm.name}]: ${{\n          \"cause\": error\n        }}`);\n      }\n    }\n  }\n  handlerFilesOfForm(files, sizeFile) {\n    const formData = new FormData();\n    // Drap&Drop - Receive files.\n    Array.from(files).forEach(file => {\n      for (let i = 0; i < file.size; i += sizeFile) {\n        formData.append(file.name, file.slice(i, i + sizeFile));\n      }\n      ;\n    });\n    // Drap&Drop - Receive CSRF token\n    const csrftokenHtml = document.querySelector(\"[name='csrfmiddlewaretoken'\");\n    if (!csrftokenHtml) return;\n    formData.append(csrftokenHtml.name, csrftokenHtml.value);\n    return formData;\n  }\n  __handlerOfButtom(event, text = \"Sending\") {\n    /**\n     * This method work with a buttom of form.\n     * @param text: string - text of buttom. Default: \"Sending\".\n     * @retrun void.\n     */\n    try {\n      let target = event.target;\n      while (target && target.id && target.id !== \"download-drop-zone\") {\n        target = target.parentElement;\n      }\n      ;\n      if (!target) return;\n      const buttomHtml = target.querySelector(\"button\");\n      if (!buttomHtml) return;\n      if (buttomHtml.textContent.length > 10) {\n        buttomHtml.classList.add(\"active\");\n        this.__textButtomOfForm = buttomHtml.innerHTML;\n        buttomHtml.innerHTML = \"\";\n        buttomHtml.insertAdjacentText(\"beforeend\", text);\n      } else {\n        buttomHtml.innerHTML = \"\";\n        if (text.toLowerCase().includes(\"error\")) {\n          buttomHtml.insertAdjacentText(\"beforeend\", text);\n        } else {\n          buttomHtml.insertAdjacentHTML(\"beforeend\", this.__textButtomOfForm);\n          buttomHtml.classList.remove(\"active\");\n        }\n      }\n    } catch (error) {\n      if (error instanceof Error) {\n        throw new Error(`[${this.logTemplText}][${this.__handlerOfButtom.name}]: ${{\n          \"cause\": error\n        }}`);\n      }\n    }\n  }\n  cleanerOfFormes(event) {\n    // Clean a form.\n    const currentTarget = event.currentTarget;\n    if (!currentTarget) return;\n    currentTarget.reset();\n  }\n  async requestPost(formData) {\n    /**\n     * Drap&Drop - Here we send files to the server.\n     * @param formData: FormData - form data for request.\n     * @return Promise<Boolean | JsonSourceFile> - false or data of json/object.\n     */\n    try {\n      const response = await fetch(pathname, {\n        method: \"POST\",\n        body: formData\n      });\n      if (response.ok) {\n        console.log(\"Files was sent successfully!\");\n        const data = await response.json();\n        if (data) return data;\n      } else console.log(\"Files was not sent!\");\n    } catch (error) {\n      if (error instanceof Error) {\n        throw new Error(`[${this.logTemplText}][${this.requestPost.name}]: ${{\n          \"cause\": error\n        }}`);\n      }\n    }\n    return false;\n  }\n}\n;\n\n\n//# sourceURL=webpack://shoop-admin-download/./src/load_catalog/index.ts?\n}");

/***/ }

/******/ 	});
/************************************************************************/
/******/ 	// The module cache
/******/ 	var __webpack_module_cache__ = {};
/******/ 	
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/ 		// Check if module is in cache
/******/ 		var cachedModule = __webpack_module_cache__[moduleId];
/******/ 		if (cachedModule !== undefined) {
/******/ 			return cachedModule.exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = __webpack_module_cache__[moduleId] = {
/******/ 			// no module.id needed
/******/ 			// no module.loaded needed
/******/ 			exports: {}
/******/ 		};
/******/ 	
/******/ 		// Execute the module function
/******/ 		if (!(moduleId in __webpack_modules__)) {
/******/ 			delete __webpack_module_cache__[moduleId];
/******/ 			var e = new Error("Cannot find module '" + moduleId + "'");
/******/ 			e.code = 'MODULE_NOT_FOUND';
/******/ 			throw e;
/******/ 		}
/******/ 		__webpack_modules__[moduleId](module, module.exports, __webpack_require__);
/******/ 	
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = __webpack_require__("./src/index.ts");
/******/ 	
/******/ })()
;