import React, { Component } from "react";

class Counter extends React.Component {
  render() {
    const { onIncrement, onDelete, onDecrement, counter } = this.props;
    return (
      <div>
        <div className="container">
          <div className="row">
            <div className="col-1">
              <span className={this.getBadgeClasses()}>
                {this.formatCount()}
              </span>
            </div>
            <div className="col">
              <button
                onClick={() => onIncrement(counter)}
                className="btn btn-secondary btn-sm m-2"
              >
                +
              </button>
              <button
                onClick={() => {
                  counter.value && onDecrement(counter);
                }}
                className="btn btn-secondary btn-sm"
                disabled={!counter.value}
              >
                -
              </button>
              <button
                onClick={() => onDelete(counter.id)}
                className="btn btn-danger btn-sm m-2"
              >
                X
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  getBadgeClasses() {
    let classes = "badge m-2 bg-";
    classes += this.props.counter.value === 0 ? "warning" : "primary";
    return classes;
  }

  formatCount() {
    const { value: count } = this.props.counter;
    return count === 0 ? "Zero" : count;
  }
}

export default Counter;
