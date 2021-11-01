import React, { Component } from "react";
import { getMovies } from "../services/fakeMovieService";

class Movies extends React.Component {
  state = {
    movies: getMovies(),
  };

  handleDelete = (movie) => {
    let arrayCopy = this.state.movies.filter((row) => row._id != movie);
    this.setState({ movies: arrayCopy });
  };

  render() {
    return (
      <div>
        <h1 style={{ margin: "1rem" }}>{this.header()}</h1>
        <table
          style={{
            margin: "1rem",
            width: "80%",
            borderTop: "2px solid #b3b3b3",
          }}
        >
          <tr>
            <th style={{ padding: "0.8rem", paddingRight: "5rem" }}>Title</th>
            <th>Genre</th>
            <th>Stock</th>
            <th>Rate</th>
          </tr>
          {this.state.movies.map((movie) => (
            <tr style={{ borderTop: "2px solid #d9d9d9" }}>
              <td style={{ padding: "0.8rem" }}>{movie.title}</td>
              <td>{movie.genre.name}</td>
              <td>{movie.numberInStock}</td>
              <td>{movie.dailyRentalRate}</td>
              <td>
                <button
                  onClick={() => this.handleDelete(movie._id)}
                  className="btn btn-danger"
                  style={{ marginRight: "-35px", paddingRight: "14px" }}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </table>
      </div>
    );
  }

  header() {
    let temp = this.state.movies.length === 0 ? "no" : this.state.movies.length;
    let title = `There's ${temp} movies in the database.`;
    return title;
  }
}

export default Movies;
