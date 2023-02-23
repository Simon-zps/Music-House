import React from "react";
import JoinRoom from "./JoinRoom";
import CreateRoom from "./CreateRoom";
import { BrowserRouter as Router, Route, Routes, Redirect, Link } from 'react-router-dom'

export default function Home() {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<p>DUPA routing</p>} />
                <Route path="/join-room" element={<JoinRoom />} />
                <Route path="/create-room" element={<CreateRoom />} />
            </Routes>
        </Router>
    );
}
