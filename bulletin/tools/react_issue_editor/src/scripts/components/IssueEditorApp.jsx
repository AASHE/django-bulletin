/**
 * @jsx React.DOM
 */

'use strict';

var React = require('react/addons');
var Panel = require('react-bootstrap/Panel');

var Sortable = {
  getDefaultProps: function() {
    return {
      "data-id" : this.props.key,
      draggable : true,
      onDragEnd: this.sortEnd.bind(this),
      onDragOver: this.dragOver.bind(this),
      onDragStart: this.sortStart.bind(this)
    }
  },
  update: function(to, from) {
    var data = this.props.data.items;
    data.splice(to, 0, data.splice(from,1)[0]);
    this.props.sort(data, to);
  },
  sortEnd: function() {
    this.props.sort(this.props.data.items, undefined);
  },
  sortStart: function(e) {
    this.dragged = e.currentTarget.dataset ?
      e.currentTarget.dataset.id :
      e.currentTarget.getAttribute('data-id');
    e.dataTransfer.effectAllowed = 'move';
    try {
      e.dataTransfer.setData('text/html', null);
    } catch (ex) {
      e.dataTransfer.setData('text', '');
    }
  },
  move: function(over,append) {
    var to = Number(over.dataset.id);
    var from = this.props.data.dragging != undefined ? this.props.data.dragging : Number(this.dragged);
    if(append) to++;
    if(from < to) to--;
    this.update(to,from);
  },
  dragOver: function(e) {
    e.preventDefault();
    var over = e.currentTarget
    var relX = e.clientX - over.getBoundingClientRect().left;
    var relY = e.clientY - over.getBoundingClientRect().top;
    var height = over.offsetHeight / 2;
    var placement = this.placement ? this.placement(relX, relY, over) : relY > height
    this.move(over, placement);
  },
  isDragging: function() {
    return this.props.data.dragging == this.props.key
  }
};

// Export React so the devtools can find it
(window !== window.top ? window.top : window).React = React;

var dragging;

var SortableListItem = React.createClass({
  mixins: [Sortable],

  render: function() {
    return this.transferPropsTo(
      <li className={this.isDragging() ? "dragging" : ""}>{this.props.item}</li>
    );
  }
});

var PostListItem = React.createClass({
  mixins: [Sortable],

  render: function() {
    return this.transferPropsTo(
      <li className={this.isDragging() ? "dragging" : ""}>
        {this.props.headline}
      </li>
    )
  }
});

var PostList = React.createClass({

  getInitialState: function() {
    return {data: this.props.data};
  },

  sort: function(items, dragging) {
    var data = this.state.data;
    data.items = items;
    data.dragging = dragging;
    this.setState({data: data});
  },

  render: function() {
    return this.transferPropsTo(
      <div className="post-list">
        <ul>
        <PostListItem headline="Man Bites Dog"
                       data={this.props.data}
                       key='man.bites.dog' />
        <PostListItem headline="Cat Leaves"
                       data={this.props.data}
                       key='cat.leaves' />
        </ul>
      </div>
    )
  }
});

var SectionPanel = React.createClass({
  mixins: [Sortable],

  render: function() {
    var key = "{this.props.name}" + "postlist";
    return this.transferPropsTo(
      <div className="section-panel">
        <Panel header={this.props.name}>
          <PostList data={this.props.data}
                    key='{key}' />
        </Panel>
      </div>
    )
  }
});

var IssueEditorApp = React.createClass({

  getInitialState: function() {
    return {data: this.props.data};
  },

  sort: function(items, dragging) {
    var data = this.state.data;
    data.items = items;
    data.dragging = dragging;
    this.setState({data: data});
  },

  render: function() {
    var listItems = this.state.data.items.map(function(item, i) {
      return (
        <SortableListItem
          sort={this.sort}
          data={this.state.data}
          key={i}
          item={item}
        />
      )
    }, this);

    return (
      <div id="issueEditor">
        <SectionPanel name="Administration" data={this.state.data}
                      key="administration" />
        <SectionPanel name="Planning" data={this.state.data}
                      key="planning" />
        <ul>{listItems}</ul>
      </div>);
    }
});

var data = {
  items: [
    "Gold",
    "Krimson",
    "Hotpink",
    "Blueviolet",
    "Cornflowerblue",
    "Skyblue",
    "Lightblue",
    "Aquamarine",
    "Burlywood"
  ]
};

React.renderComponent(<IssueEditorApp data={data}/>,
                      document.getElementById('content'));

module.exports = IssueEditorApp;
