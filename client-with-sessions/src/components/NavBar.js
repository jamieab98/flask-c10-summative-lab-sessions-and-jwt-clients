import React from "react";
import { Link } from "react-router-dom";
import styled from "styled-components";
import { Button } from "../styles";

function NavBar({ user, setUser }) {
  function handleLogoutClick() {
    fetch("/logout", { method: "DELETE" }).then((r) => {
      if (r.ok) {
        setUser(null);
      }
    });
  }

  /*function handleDoSomethingClick() {
    fetch("/newpost",{
      method: "POST",
      credentials: "include",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        title: "New Post Title",
        content: "New Post Content"
      }),
    })
    .then((response) => {
      return response.json()
    })
    .then((data) => {
      console.log("server response:", data)
    })
    .catch((error) => {
      console.log("Error:", error)
    })
  }
  */

  /*function handleDoSomethingClick() {
    fetch(`/updatenotecontent/2`, {
      method: "PATCH",
      credentials: "include",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        updatedContent: "Updated Post Content"
      }),
    })
    .then((response) => {
      return response.json()
    })
    .then((data) => {
      console.log(data)
    })
    .catch((error) => {
      console.log("Error:", error)
    })
  }
  */

  function handleDoSomethingClick() {
    fetch("/userpost?page=1&per_page=5", {
      method: "GET",
      credentials: "include"
    })
    .then((response) => {
      return response.json()
    })
    .then((data) => {
      console.log(data)
    })
    .catch((error) => {
      console.log(error)
    })
  }
  

  return (
    <Wrapper>
      <Logo>
        <Link to="/">My App</Link>
      </Logo>
      <Nav>
        <Button onClick={handleDoSomethingClick}>
          Do Something
        </Button>
        <Button variant="outline" onClick={handleLogoutClick}>
          Logout
        </Button>
      </Nav>
    </Wrapper>
  );
}

const Wrapper = styled.header`
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 8px;
`;

const Logo = styled.h1`
  font-family: "Permanent Marker", cursive;
  font-size: 3rem;
  color: deeppink;
  margin: 0;
  line-height: 1;

  a {
    color: inherit;
    text-decoration: none;
  }
`;

const Nav = styled.nav`
  display: flex;
  gap: 4px;
  position: absolute;
  right: 8px;
`;

export default NavBar;
