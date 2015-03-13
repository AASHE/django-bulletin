'use strict';

describe('Main', function () {
  var DoftaApp, component;

  beforeEach(function () {
    var container = document.createElement('div');
    container.id = 'content';
    document.body.appendChild(container);

    DoftaApp = require('../../../src/scripts/components/DoftaApp.jsx');
    component = DoftaApp();
  });

  it('should create a new instance of DoftaApp', function () {
    expect(component).toBeDefined();
  });
});
