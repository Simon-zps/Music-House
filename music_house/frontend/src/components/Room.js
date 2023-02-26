import React from "react";
import { useParams } from 'react-router-dom';
import { useState } from "react";

export default function Room() {
    let {code} = useParams();
    const [votesToSkip, setVotesToSkip] = useState(2);
    const [guestPausePermission, setGuestPausePermission] = useState(true);
    const [isHost, setIsHost] = useState(true);
    //We need to fetch data regarding that code and display info
    fetch(`/api/room/${code}`,{
        method:'GET',
        headers:{
            'Content-Type':'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        setGuestPausePermission(data.guest_pause_permission);
        setIsHost(data.is_host);
        setVotesToSkip(data.votes_to_skip);
        console.log(data)
    })

    return (
        <div id="room-info">
            <p>Room code: {code}</p>
            <p>Guest can pause: {guestPausePermission.toString()}</p>
            <p>Votes to skip: {votesToSkip}</p>
            <p>Is Host: {isHost.toString()}</p>
        </div>
    );
}