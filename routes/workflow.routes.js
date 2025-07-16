import { Router } from "express";

const workflowRouter = Router();
workflowRouter.get("/", (req, res) => {
  res.send("Workflow");
});
export default workflowRouter;
