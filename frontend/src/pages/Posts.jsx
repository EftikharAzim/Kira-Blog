import React, { useEffect, useState } from 'react';
import Container from '@mui/material/Container';
import Typography from '@mui/material/Typography';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import CardActions from '@mui/material/CardActions';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Grid from '@mui/material/Grid';
import Alert from '@mui/material/Alert';

export default function Posts() {
  const [posts, setPosts] = useState([]);
  const [error, setError] = useState('');
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [success, setSuccess] = useState('');
  const [editingId, setEditingId] = useState(null);
  const [editTitle, setEditTitle] = useState('');
  const [editContent, setEditContent] = useState('');
  const isLoggedIn = !!localStorage.getItem('access_token');

  useEffect(() => {
    fetchPosts();
    // eslint-disable-next-line
  }, []);

  const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

  const fetchPosts = async () => {
    try {
      const res = await fetch(`${API_URL}/posts`);
      const data = await res.json();
      if (res.ok) {
        setPosts(data.posts || []);
      } else {
        setError(data.msg || 'Failed to fetch posts');
      }
    } catch (err) {
      setError('Network error');
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    try {
      const res = await fetch(`${API_URL}/posts`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        },
        body: JSON.stringify({ title, content })
      });
      const data = await res.json();
      if (res.ok) {
        setSuccess('Post created!');
        setTitle('');
        setContent('');
        fetchPosts();
      } else {
        setError(data.msg || 'Failed to create post');
      }
    } catch (err) {
      setError('Network error');
    }
  };

  const startEdit = (post) => {
    setEditingId(post.id);
    setEditTitle(post.title);
    setEditContent(post.content);
  };

  const handleEdit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    try {
      const res = await fetch(`${API_URL}/posts/${editingId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        },
        body: JSON.stringify({ title: editTitle, content: editContent })
      });
      const data = await res.json();
      if (res.ok) {
        setSuccess('Post updated!');
        setEditingId(null);
        fetchPosts();
      } else {
        setError(data.msg || 'Failed to update post');
      }
    } catch (err) {
      setError('Network error');
    }
  };

  const handleDelete = async (id) => {
    setError('');
    setSuccess('');
    try {
      const res = await fetch(`${API_URL}/posts/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': 'Bearer ' + localStorage.getItem('access_token')
        }
      });
      const data = await res.json();
      if (res.ok) {
        setSuccess('Post deleted!');
        fetchPosts();
      } else {
        setError(data.msg || 'Failed to delete post');
      }
    } catch (err) {
      setError('Network error');
    }
  };

  return (
    <Container maxWidth="md">
      <Typography variant="h4" gutterBottom>Posts</Typography>
      {isLoggedIn && (
        <form onSubmit={handleCreate} style={{marginBottom: '2rem'}}>
          <Typography variant="h6">Create a Post</Typography>
          <TextField
            label="Title"
            value={title}
            onChange={e => setTitle(e.target.value)}
            required
            fullWidth
            sx={{ mb: 2 }}
          />
          <TextField
            label="Content"
            value={content}
            onChange={e => setContent(e.target.value)}
            required
            fullWidth
            multiline
            rows={3}
            sx={{ mb: 2 }}
          />
          <Button type="submit" variant="contained">Create</Button>
          {success && <Alert severity="success" sx={{ mt: 2 }}>{success}</Alert>}
        </form>
      )}
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}
      <Grid container spacing={2}>
        {posts.map(post => (
          <Grid item xs={12} sm={6} md={4} key={post.id}>
            <Card variant="outlined" sx={{ mb: 2 }}>
              <CardContent>
                {editingId === post.id ? (
                  <form onSubmit={handleEdit}>
                    <TextField
                      label="Title"
                      value={editTitle}
                      onChange={e => setEditTitle(e.target.value)}
                      required
                      fullWidth
                      sx={{ mb: 1 }}
                    />
                    <TextField
                      label="Content"
                      value={editContent}
                      onChange={e => setEditContent(e.target.value)}
                      required
                      fullWidth
                      multiline
                      rows={2}
                      sx={{ mb: 1 }}
                    />
                    <Button type="submit" variant="contained" size="small">Save</Button>
                    <Button type="button" onClick={() => setEditingId(null)} size="small" sx={{ ml: 1 }}>Cancel</Button>
                  </form>
                ) : (
                  <>
                    <Typography variant="h6">{post.title}</Typography>
                    <Typography variant="body2" color="text.secondary">{post.content}</Typography>
                    <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 1 }}>By {post.author} on {post.created_at}</Typography>
                  </>
                )}
              </CardContent>
              {isLoggedIn && editingId !== post.id && (
                <CardActions>
                  <Button onClick={() => startEdit(post)} size="small">Edit</Button>
                  <Button onClick={() => handleDelete(post.id)} size="small" color="error">Delete</Button>
                </CardActions>
              )}
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
}
