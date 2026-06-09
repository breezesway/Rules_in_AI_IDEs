import request from 'supertest';
import app from '../src/app';
import { createTestProject, createTestBug } from '../src/test/setup';

describe('Projects API', () => {
  describe('GET /api/projects', () => {
    it('should return empty array when no projects exist', async () => {
      const response = await request(app)
        .get('/api/projects')
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toEqual([]);
      expect(response.body.message).toContain('Retrieved 0 projects');
    });

    it('should return all projects with bug counts', async () => {
      // Create test projects
      const project1 = await createTestProject('Project 1');
      const project2 = await createTestProject('Project 2');
      
      // Add bugs to project1
      await createTestBug(project1.id);
      await createTestBug(project1.id);

      const response = await request(app)
        .get('/api/projects')
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toHaveLength(2);
      expect(response.body.data[0]).toMatchObject({
        id: expect.any(Number),
        name: expect.any(String),
        createdAt: expect.any(String),
        bugCount: expect.any(Number),
      });
      
      // Find project1 in response and check bug count
      const project1Response = response.body.data.find((p: any) => p.id === project1.id);
      expect(project1Response.bugCount).toBe(2);
      
      const project2Response = response.body.data.find((p: any) => p.id === project2.id);
      expect(project2Response.bugCount).toBe(0);
    });
  });

  describe('GET /api/projects/:id', () => {
    it('should return project by ID', async () => {
      const project = await createTestProject('Test Project');

      const response = await request(app)
        .get(`/api/projects/${project.id}`)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toMatchObject({
        id: project.id,
        name: 'Test Project',
        createdAt: expect.any(String),
      });
    });

    it('should return 404 for non-existent project', async () => {
      const response = await request(app)
        .get('/api/projects/999')
        .expect(404);

      expect(response.body.success).toBe(false);
      expect(response.body.error.code).toBe('NOT_FOUND');
      expect(response.body.error.message).toContain('Project with id 999 not found');
    });

    it('should return 400 for invalid project ID', async () => {
      const response = await request(app)
        .get('/api/projects/invalid')
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.error.code).toBe('VALIDATION_ERROR');
    });
  });

  describe('POST /api/projects', () => {
    it('should create a new project', async () => {
      const projectData = { name: 'New Project' };

      const response = await request(app)
        .post('/api/projects')
        .send(projectData)
        .expect(201);

      expect(response.body.success).toBe(true);
      expect(response.body.data).toMatchObject({
        id: expect.any(Number),
        name: 'New Project',
        createdAt: expect.any(String),
      });
      expect(response.body.message).toBe('Project created successfully');
    });

    it('should trim whitespace from project name', async () => {
      const projectData = { name: '  Trimmed Project  ' };

      const response = await request(app)
        .post('/api/projects')
        .send(projectData)
        .expect(201);

      expect(response.body.data.name).toBe('Trimmed Project');
    });

    it('should return 400 for missing project name', async () => {
      const response = await request(app)
        .post('/api/projects')
        .send({})
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.error.code).toBe('VALIDATION_ERROR');
    });

    it('should return 400 for empty project name', async () => {
      const response = await request(app)
        .post('/api/projects')
        .send({ name: '' })
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.error.code).toBe('VALIDATION_ERROR');
    });

    it('should return 400 for project name too long', async () => {
      const longName = 'a'.repeat(256);
      
      const response = await request(app)
        .post('/api/projects')
        .send({ name: longName })
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.error.code).toBe('VALIDATION_ERROR');
    });

    it('should return 400 for project name with invalid characters', async () => {
      const response = await request(app)
        .post('/api/projects')
        .send({ name: 'Project<script>alert("xss")</script>' })
        .expect(400);

      expect(response.body.success).toBe(false);
      expect(response.body.error.code).toBe('VALIDATION_ERROR');
    });
  });

  describe('PUT /api/projects/:id', () => {
    it('should update project name', async () => {
      const project = await createTestProject('Original Name');
      const updates = { name: 'Updated Name' };

      const response = await request(app)
        .put(`/api/projects/${project.id}`)
        .send(updates)
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.name).toBe('Updated Name');
      expect(response.body.message).toBe('Project updated successfully');
    });

    it('should return 404 for non-existent project', async () => {
      const response = await request(app)
        .put('/api/projects/999')
        .send({ name: 'Updated Name' })
        .expect(404);

      expect(response.body.success).toBe(false);
      expect(response.body.error.code).toBe('NOT_FOUND');
    });

    it('should handle empty update (no changes)', async () => {
      const project = await createTestProject('Test Project');

      const response = await request(app)
        .put(`/api/projects/${project.id}`)
        .send({})
        .expect(200);

      expect(response.body.success).toBe(true);
      expect(response.body.data.name).toBe('Test Project');
    });
  });

  describe('DELETE /api/projects/:id', () => {
    it('should delete project', async () => {
      const project = await createTestProject('Project to Delete');

      const response = await request(app)
        .delete(`/api/projects/${project.id}`)
        .expect(204);

      expect(response.body).toEqual({});

      // Verify project is deleted
      await request(app)
        .get(`/api/projects/${project.id}`)
        .expect(404);
    });

    it('should delete project and cascade delete bugs', async () => {
      const project = await createTestProject('Project with Bugs');
      await createTestBug(project.id);
      await createTestBug(project.id);

      await request(app)
        .delete(`/api/projects/${project.id}`)
        .expect(204);

      // Verify project and bugs are deleted
      await request(app)
        .get(`/api/projects/${project.id}`)
        .expect(404);
    });

    it('should return 404 for non-existent project', async () => {
      const response = await request(app)
        .delete('/api/projects/999')
        .expect(404);

      expect(response.body.success).toBe(false);
      expect(response.body.error.code).toBe('NOT_FOUND');
    });
  });
});