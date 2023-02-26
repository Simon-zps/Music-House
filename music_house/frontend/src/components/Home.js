import React from "react";
import JoinRoom from "./JoinRoom";
import CreateRoom from "./CreateRoom";
import Room from "./Room";
import { BrowserRouter as Router, Route, Routes, Redirect, Link } from 'react-router-dom'

export default function Home() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<p>Home</p>} />
                <Route path="/join-room" element={<JoinRoom />} />
                <Route path="/create-room" element={<CreateRoom />} />
                <Route path="/room/:code" element={<Room />} />
            </Routes>
        </Router>
    );
}
