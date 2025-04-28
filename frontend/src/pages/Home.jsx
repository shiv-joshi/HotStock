import { useState, useEffect } from "react";
import api from "../api";
import "../styles/Home.css";
import HighScore from "../components/HighScore";

function Home() {
  const [ticker, setTicker] = useState("");
  const [profile, setProfile] = useState(null);
  const [profiles, setProfiles] = useState([]);
  const sortedProfiles = [...profiles].sort((a, b) => b.score - a.score);
  const [predicted, setPredicted] = useState(false); // set it based on a backend value
  const [last, setLast] = useState("No prediction!");

  useEffect(() => {
    getProfile();
    getProfiles();
    getDailyTicker();
    getPrevPrediction();
  }, []);

  // Get current user;s profile
  const getProfile = () => {
    api.get("api/profile/").then((res) => {
      setProfile(res.data);
      setPredicted(res.data.predicted);
    });
  };

  // Get all profiles for leaderboard
  const getProfiles = () => {
    api.get("api/profiles/").then((res) => {
      setProfiles(res.data);
    });
  };

  // Get current user's last prediction
  const getPrevPrediction = () => {
    api.get("api/prev-prediction/").then((res) => {
      setLast(res.data.last);
    });
  };

  // Get random stock of the day
  const getDailyTicker = () => {
    api.get("api/ticker/").then((res) => setTicker(res.data.symbol));
  };

  // Log users prediction for stock
  const createPrediction = async (choice) => {
    api.post("api/predict/", { prediction: choice });
    alert("Prediction submitted!");
  };

  return (
    <div>
      {profile ? (
        <>
          <div class="dashboard">
            <h3>User: {profile.username}</h3>
            <h3>Score: {profile.score}</h3>
          </div>
          <p class="last-guess">{last}</p>
        </>
      ) : (
        <h3>Please Login</h3>
      )}
      <form>
        <h2>{ticker}</h2>
        {!predicted ? (
          <div class="button-container">
            <button
              onClick={() => createPrediction("rise")}
              class="rise-button"
            >
              RISE
            </button>
            <button
              onClick={() => createPrediction("fall")}
              class="fall-button"
            >
              FALL
            </button>
          </div>
        ) : (
          <p>✅ Prediction submitted for today!</p>
        )}

        <div class="leaderboard">
          <div class="canvas">
            <div id="card">
              <div class="card-content">
                <p id="title" class="highlight">LEADERBOARD</p>
                <div class="rankings">
                  {sortedProfiles.map((p) => (
                    <HighScore highScorer={p} id={p.id} />
                  ))}
                </div>
                <div class="corner-elements">
                  <span></span><span></span><span></span><span></span>
                </div>
                <div class="scan-line"></div>
              </div>
            </div>
          </div>
        </div>

      </form>
    </div>
  );
}

export default Home;
