Used along with selenium to identify Shadow Elements present under Shadow DOM.

The Structure of shadow DOM would be as below:

Shadow Host -> Shadow Root -> Shadow DOM Elements

check the shadow dom by inspecting the website here:

https://shrinivasbb.github.io/ShadowDomSite

Use this module to get Shadow DOM Elements matching the CSS selectors.

For usage check the below link:

https://github.com/shrinivasbb/shadowselenium


For implementation check the tests folder.


.. code-block:: python

    from shadowselenium import ShadowElement

    shadowdom = ShadowElement(driver) #argument should be driver instance of opened browser i.e chromedriver etc.

    shadowelement = shadowdom.find_shadow_element_by_css("shadow-hostnav", ".nav-link")   
    

