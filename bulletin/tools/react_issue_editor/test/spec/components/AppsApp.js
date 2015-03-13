'use strict';

describe('Main', function () {
  var AppsApp, component;

  beforeEach(function () {
    var container = document.createElement('div');
    container.id = 'content';
    document.body.appendChild(container);

    AppsApp = require('../../../src/scripts/components/AppsApp.jsx');
    component = AppsApp();
  });

  it('should create a new instance of AppsApp', function () {
    expect(component).toBeDefined();
  });
});
