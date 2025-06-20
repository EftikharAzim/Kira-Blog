import React, { useEffect, useState } from 'react';

export default function Profile() {
  const [user, setUser] = useState(null);
  const [posts, setPosts] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchProfile = async () => {
      const token = localStorage.getItem('access_token');
      if (!token) return;
      try {
        // Get user info from token (decode JWT payload)
        const payload = JSON.parse(atob(token.split('.')[1]));
        setUser({ id: payload.sub || payload.identity });
        // Fetch user's posts
        const res = await fetch('http://localhost:5000/posts');
        const data = await res.json();
        if (res.ok) {
          // Filter posts by user id
          setPosts((data.posts || []).filter(p => String(p.author) === String(payload.sub || payload.identity)));
        } else {
          setError(data.msg || 'Failed to fetch posts');
        }
      } catch (err) {
        setError('Network error');
      }
    };
    fetchProfile();
  }, []);

  if (!user) return <div className="container"><h2>Profile</h2><p>Please log in to view your profile.</p></div>;

  return (
    <div className="container">
      <h2>Profile</h2>
      <p><b>User ID:</b> {user.id}</p>
      <h3>Your Posts</h3>
      <ul>
        {posts.length === 0 && <li>No posts yet.</li>}
        {posts.map(post => (
          <li key={post.id}>
            <h4>{post.title}</h4>
            <p>{post.content}</p>
            <small>{post.created_at}</small>
          </li>
        ))}
      </ul>
      {error && <p style={{color:'red'}}>{error}</p>}
    </div>
  );
}
