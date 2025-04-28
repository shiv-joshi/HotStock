import React from "react";
import "../styles/HighScore.css"

function HighScore({ highScorer }) {
    return (
            <p>{highScorer.user.username} - {highScorer.score}</p>
    );
}

export default HighScore