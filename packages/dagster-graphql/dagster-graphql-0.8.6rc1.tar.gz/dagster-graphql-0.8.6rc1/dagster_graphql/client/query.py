ERROR_FRAGMENT = '''
fragment errorFragment on PythonError {
  message
  className
  stack
  cause {
    message
    className
    stack
    cause {
      message
      className
      stack
    }
  }
}
'''

STEP_EVENT_FRAGMENTS = (
    ERROR_FRAGMENT
    + '''
fragment metadataEntryFragment on EventMetadataEntry {
  __typename
  label
  description
  ... on EventFloatMetadataEntry {
    value
  }
  ... on EventJsonMetadataEntry {
    jsonString
  }
  ... on EventMarkdownMetadataEntry {
    mdStr
  }
  ... on EventPathMetadataEntry {
    path
  }
  ... on EventPythonArtifactMetadataEntry {
    module
    name
  }
  ... on EventTextMetadataEntry {
    text
  }
  ... on EventUrlMetadataEntry {
    url
  }
}

fragment stepEventFragment on StepEvent {
  step {
    key
    solidHandleID
    kind
    inputs {
      name
      type {
        key
      }
      dependsOn {
        key
      }
    }
    outputs {
      name
      type {
        key
      }
    }
    metadata {
      key
      value
    }
  }

  ... on EngineEvent {
    metadataEntries {
      ...metadataEntryFragment
    }
    markerStart
    markerEnd
    engineError: error {
      ...errorFragment
    }
  }
  ... on ExecutionStepFailureEvent {
    error {
      ...errorFragment
    }
    failureMetadata {
      label
      description
      metadataEntries {
        ...metadataEntryFragment
      }
    }
  }
  ... on ExecutionStepInputEvent {
    inputName
    typeCheck {
      __typename
      success
      label
      description
      metadataEntries {
        ...metadataEntryFragment
      }
    }
  }
  ... on ExecutionStepOutputEvent {
    outputName
    typeCheck {
      __typename
      success
      label
      description
      metadataEntries {
        ...metadataEntryFragment
      }
    }
  }

  ... on ExecutionStepUpForRetryEvent {
    retryError: error {
      ...errorFragment
    }
    secondsToWait
  }

  ... on ObjectStoreOperationEvent {
        step { key }
        operationResult {
            op
            metadataEntries {
                ...metadataEntryFragment
            }
        }
    }

  ... on StepExpectationResultEvent {
    expectationResult {
      success
      label
      description
      metadataEntries {
        ...metadataEntryFragment
      }
    }
  }
  ... on StepMaterializationEvent {
    materialization {
      label
      description
      metadataEntries {
        ...metadataEntryFragment
      }
    }
  }

  ... on MessageEvent {
    runId
    message
    timestamp
    level
  }



}
'''
)

MESSAGE_EVENT_FRAGMENTS = (
    '''
fragment messageEventFragment on MessageEvent {
  runId
  message
  timestamp
  level
  ...stepEventFragment
  ... on PipelineInitFailureEvent {
    initError: error {
      ...errorFragment
    }
  }
}
'''
    + STEP_EVENT_FRAGMENTS
)

EXECUTE_RUN_IN_PROCESS_MUTATION = (
    ERROR_FRAGMENT
    + '''
mutation(
  $repositoryLocationName: String!
  $repositoryName: String!
  $runId: String!
) {
  executeRunInProcess(
    repositoryLocationName: $repositoryLocationName
    repositoryName: $repositoryName
    runId: $runId
  ) {
    __typename
    ... on ExecuteRunInProcessSuccess {
      run {
        runId
        status
        pipeline {
          name
        }

        tags {
          key
          value
        }
        runConfigYaml
        mode
      }
    }
    ... on InvalidStepError {
      invalidStepKey
    }
    ... on InvalidOutputError {
      stepKey
      invalidOutputName
    }
    ... on PipelineConfigValidationInvalid {
      pipelineName
      errors {
        __typename
        message
        path
        reason
      }
    }
    ... on PipelineNotFoundError {
      message
      pipelineName
    }
    ... on PythonError {
      ...errorFragment
    }
    ... on PipelineRunConflict {
      message
    }
    ... on PipelineRunNotFoundError {
      message
    }
    ... on ConflictingExecutionParamsError {
      message
    }
    ... on PresetNotFoundError {
      message
      preset
    }
  }
}
'''
)

EXECUTE_PLAN_MUTATION = (
    '''
mutation(
  $executionParams: ExecutionParams!
  $retries: Retries
) {
  executePlan(
    executionParams: $executionParams,
    retries: $retries,
  ) {
    __typename
    ... on InvalidStepError {
      invalidStepKey
    }
    ... on PipelineConfigValidationInvalid {
      pipelineName
      errors {
        __typename
        message
        path
        reason
      }
    }
    ... on PipelineNotFoundError {
      message
      pipelineName
    }
    ... on PythonError {
      message
      stack
    }
    ... on ExecutePlanSuccess {
      pipeline {
        name
      }
      hasFailures
      stepEvents {
        __typename
        ...stepEventFragment
      }
    }
  }
}
'''
    + STEP_EVENT_FRAGMENTS
)

RAW_EXECUTE_PLAN_MUTATION = '''
mutation(
  $executionParams: ExecutionParams!
  $retries: Retries
) {
  executePlan(
    executionParams: $executionParams,
    retries: $retries,
  ) {
    __typename
    ... on InvalidStepError {
      invalidStepKey
    }
    ... on PipelineConfigValidationInvalid {
      pipelineName
      errors {
        __typename
        message
        path
        reason
      }
    }
    ... on PipelineNotFoundError {
      message
      pipelineName
    }
    ... on PythonError {
      message
      stack
      cause {
          message
          stack
      }
    }
    ... on ExecutePlanSuccess {
      pipeline {
        name
      }
      hasFailures
      rawEventRecords
    }
  }
}
'''

SUBSCRIPTION_QUERY = (
    MESSAGE_EVENT_FRAGMENTS
    + '''
subscription subscribeTest($runId: ID!) {
  pipelineRunLogs(runId: $runId) {
    __typename
    ... on PipelineRunLogsSubscriptionSuccess {
      run {
        runId
      }
      messages {
        __typename
        ...messageEventFragment

        # only include here because unstable between runs
        ... on StepMaterializationEvent {
          materialization {
            label
            description
            metadataEntries {
              __typename
              ...metadataEntryFragment
            }
          }
        }

        ... on ExecutionStepFailureEvent {
          step {
            key
            kind
          }
          error {
            ...errorFragment
          }
        }
      }
    }

    ... on PipelineRunLogsSubscriptionFailure {
      missingRunId
      message
    }
  }
}

'''
)

LAUNCH_PIPELINE_EXECUTION_MUTATION = (
    ERROR_FRAGMENT
    + '''
mutation($executionParams: ExecutionParams!) {
  launchPipelineExecution(executionParams: $executionParams) {
    __typename

    ... on InvalidStepError {
      invalidStepKey
    }
    ... on InvalidOutputError {
      stepKey
      invalidOutputName
    }
    ... on LaunchPipelineRunSuccess {
      run {
        runId
        pipeline {
          name
        }
        tags {
          key
          value
        }
        status
        runConfigYaml
        mode
      }
    }
    ... on ConflictingExecutionParamsError {
      message
    }
    ... on PresetNotFoundError {
      preset
      message
    }
    ... on PipelineConfigValidationInvalid {
      pipelineName
      errors {
        __typename
        message
        path
        reason
      }
    }
    ... on PipelineNotFoundError {
      message
      pipelineName
    }
    ... on PythonError {
      ...errorFragment
    }
  }
}
'''
)


LAUNCH_PIPELINE_REEXECUTION_MUTATION = (
    ERROR_FRAGMENT
    + '''
mutation($executionParams: ExecutionParams!) {
  launchPipelineReexecution(executionParams: $executionParams) {
    __typename

    ... on PythonError {
      ...errorFragment
    }
    ... on LaunchPipelineRunSuccess {
      run {
        runId
        status
        pipeline {
          name
        }
        tags {
          key
          value
        }
        runConfigYaml
        mode
        rootRunId
        parentRunId
      }
    }
    ... on PipelineNotFoundError {
      message
      pipelineName
    }
    ... on PipelineConfigValidationInvalid {
      pipelineName
      errors {
        __typename
        message
        path
        reason
      }
    }
    ... on InvalidStepError {
      invalidStepKey
    }
    ... on InvalidOutputError {
      stepKey
      invalidOutputName
    }
    ... on ConflictingExecutionParamsError {
      message
    }
    ... on PresetNotFoundError {
      preset
      message
    }
  }
}
'''
)

PIPELINE_REEXECUTION_INFO_QUERY = '''
query ReexecutionInfoQuery($runId: ID!) {
  pipelineRunOrError(runId: $runId) {
    __typename
    ... on PipelineRun {
        stepKeysToExecute
      }
    }
  }
'''
